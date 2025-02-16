from typing import Dict, Any, List
import json
import logging
from datetime import datetime
from temporalio import activity
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..config import settings

logger = logging.getLogger(__name__)

@activity.defn
async def analyze_team_data(team_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze team data using OpenAI to generate insights."""
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Prepare the prompt
        prompt = f"""
        Analyze this volleyball team data and provide insights about:
        1. Team composition and experience level
        2. Geographic distribution of players
        3. Notable strengths based on positions
        4. Coaching experience and structure

        Team Data:
        {json.dumps(team_data, indent=2)}
        """

        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a volleyball analytics expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        analysis = response.choices[0].message.content

        return {
            "team_data": team_data,
            "ai_analysis": analysis,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in AI analysis: {str(e)}")
        raise

@activity.defn
async def store_in_sheets(analyzed_data: Dict[str, Any]) -> str:
    """Store the analyzed team data in Google Sheets."""
    try:
        creds = Credentials.from_authorized_user_info(
            json.loads(settings.GOOGLE_CREDENTIALS),
            ['https://www.googleapis.com/auth/spreadsheets']
        )

        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = service.spreadsheets()

        # Prepare the data
        team_data = analyzed_data["team_data"]
        analysis = analyzed_data["ai_analysis"]
        timestamp = analyzed_data["analysis_timestamp"]

        # Format data for sheets
        team_info = [
            ["Team Information", timestamp],
            ["School", team_data["school_name"]],
            ["Division", team_data["division"]],
            ["Conference", team_data["conference"]],
            ["Location", team_data["location"]],
            [""],
            ["AI Analysis"],
            [analysis],
            [""],
            ["Roster"],
            ["Name", "Number", "Position", "Year", "Hometown", "Height"]
        ]

        # Add player data
        for player in team_data["players"]:
            team_info.append([
                player["name"],
                player["number"],
                player["position"],
                player["year"],
                player["hometown"],
                player["height"]
            ])

        # Add coaching staff
        team_info.extend([
            [""],
            ["Coaching Staff"],
            ["Name", "Title"]
        ])
        
        if team_data.get("head_coach"):
            team_info.append([
                team_data["head_coach"]["name"],
                team_data["head_coach"]["title"]
            ])
        
        for coach in team_data.get("assistant_coaches", []):
            team_info.append([coach["name"], coach["title"]])

        # Update or create sheet
        sheet_id = settings.GOOGLE_SHEET_ID
        range_name = f"{team_data['school_name']}!A1"
        
        result = spreadsheet.values().update(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption='RAW',
            body={'values': team_info}
        ).execute()

        return f"Updated {result.get('updatedCells')} cells in Google Sheets"
    except Exception as e:
        logger.error(f"Error storing in Google Sheets: {str(e)}")
        raise 