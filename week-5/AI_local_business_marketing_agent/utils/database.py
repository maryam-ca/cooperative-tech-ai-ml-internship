"""
Database Manager - Handle campaign data persistence
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from pathlib import Path

from config.settings import DATABASE_CONFIG

class DatabaseManager:
    """Manage database operations for campaigns and analytics"""
    
    def __init__(self):
        self.db_path = DATABASE_CONFIG['path']
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                platform TEXT NOT NULL,
                business_type TEXT NOT NULL,
                content TEXT,
                status TEXT DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                published_at TIMESTAMP,
                metadata TEXT,
                engagement_data TEXT
            )
        ''')
        
        # Create analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                date DATE,
                metric_name TEXT,
                metric_value REAL,
                FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
            )
        ''')
        
        # Create templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_campaign(self, campaign_data: Dict) -> int:
        """Save a campaign to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO campaigns 
            (name, type, platform, business_type, content, status, metadata, engagement_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            campaign_data.get('name', 'Unnamed Campaign'),
            campaign_data.get('type', 'promotional'),
            campaign_data.get('platform', 'social_media'),
            campaign_data.get('business_type', 'shop'),
            campaign_data.get('content', ''),
            campaign_data.get('status', 'draft'),
            json.dumps(campaign_data.get('metadata', {})),
            json.dumps(campaign_data.get('engagement', {}))
        ))
        
        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return campaign_id
    
    def get_campaigns(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get campaigns with optional filters"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        query = "SELECT * FROM campaigns"
        params = []
        
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY created_at DESC"
        
        cursor = conn.execute(query, params)
        results = []
        
        for row in cursor.fetchall():
            campaign = dict(row)
            campaign['metadata'] = json.loads(campaign['metadata']) if campaign['metadata'] else {}
            campaign['engagement_data'] = json.loads(campaign['engagement_data']) if campaign['engagement_data'] else {}
            results.append(campaign)
        
        conn.close()
        return results
    
    def update_campaign(self, campaign_id: int, updates: Dict) -> bool:
        """Update a campaign"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        set_clause = []
        params = []
        
        for key, value in updates.items():
            if key == 'metadata':
                value = json.dumps(value)
            elif key == 'engagement':
                key = 'engagement_data'
                value = json.dumps(value)
            
            set_clause.append(f"{key} = ?")
            params.append(value)
        
        params.append(campaign_id)
        query = f"UPDATE campaigns SET {', '.join(set_clause)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def delete_campaign(self, campaign_id: int) -> bool:
        """Delete a campaign"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM campaigns WHERE id = ?", (campaign_id,))
        deleted = cursor.rowcount
        cursor.execute("DELETE FROM analytics WHERE campaign_id = ?", (campaign_id,))
        
        success = deleted > 0
        conn.commit()
        conn.close()
        return success
    
    def save_analytics(self, campaign_id: int, metrics: Dict) -> None:
        """Save analytics data for a campaign"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date = datetime.now().date().isoformat()
        
        for metric_name, metric_value in metrics.items():
            cursor.execute('''
                INSERT INTO analytics (campaign_id, date, metric_name, metric_value)
                VALUES (?, ?, ?, ?)
            ''', (campaign_id, date, metric_name, metric_value))
        
        conn.commit()
        conn.close()
    
    def get_analytics(self, campaign_id: int) -> pd.DataFrame:
        """Get analytics data for a campaign"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT date, metric_name, metric_value FROM analytics WHERE campaign_id = ? ORDER BY date"
        df = pd.read_sql_query(query, conn, params=(campaign_id,))
        conn.close()
        return df
    
    def get_campaign_performance(self, days: int = 30) -> Dict:
        """Get overall campaign performance for recent days"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                c.type,
                c.platform,
                COUNT(c.id) as total_campaigns,
                AVG(a.metric_value) as avg_engagement
            FROM campaigns c
            LEFT JOIN analytics a ON c.id = a.campaign_id
            WHERE c.created_at >= datetime('now', ?)
            GROUP BY c.type, c.platform
        '''
        
        df = pd.read_sql_query(query, conn, params=(f'-{days} days',))
        conn.close()
        
        if df.empty:
            return {}
        
        return df.to_dict('records')