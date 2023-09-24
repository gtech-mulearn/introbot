from uuid import uuid4
from datetime import datetime
class IntroQueries:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def format_time(self,date_time):
        formated_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(formated_time, "%Y-%m-%d %H:%M:%S")

    def get_current_utc_time(self):
        return self.format_time(datetime.utcnow())

    def is_intro_done(self, discord_id: int) -> bool:
        query = """
            SELECT TRUE FROM karma_activity_log WHERE user_id = (SELECT id FROM user WHERE discord_id = :discord_id) 
            AND task_id = (SELECT id FROM task_list WHERE hashtag = :hashtag) AND appraiser_approved = 1;
        """
        params = {
            'discord_id': str(discord_id),
            'hashtag': '#intro'
        }
        return self.db_connection.fetch_single_data(query, params)

    def is_intro_started(self, discord_id: int) -> bool:
        query = """
            SELECT TRUE FROM intro_task WHERE user_id = (SELECT id FROM user WHERE discord_id = :discord_id);
        """
        params = {
            'discord_id': str(discord_id)
        }
        return self.db_connection.fetch_single_data(query, params)

    def insert_user(self, discord_id: int, channel_id: int) -> None:
        query = """
            INSERT INTO intro_task (id, user_id, channel_id, progress_id,updated_by,updated_at,created_by,created_at) 
            VALUES (:id,(SELECT id FROM user WHERE discord_id = :discord_id), :channel_id,:progress_id, (SELECT id FROM user WHERE discord_id = :discord_id),
            :updated_at, (SELECT id FROM user WHERE discord_id = :discord_id), :created_at);
        """
        params = {
            'id': str(uuid4()),
            'discord_id': str(discord_id),
            'channel_id': str(channel_id),
            'progress_id': 1,
            'updated_at': self.get_current_utc_time(),
            'created_at': self.get_current_utc_time()
        }
        self.db_connection.execute(query, params)

    def fetch_user_id_from_discord_id(self, discord_id):
        query = """
            SELECT id FROM user WHERE discord_id = :discord_id;
        """
        params = {
            'discord_id': str(discord_id)
        }
        return self.db_connection.fetch_single_data(query, params)

    def is_valid_channel(self, channel_id, user_id):
        query = """
            SELECT channel_id
            FROM intro_task
            WHERE user_id = :user_id
        """
        params = {
            'user_id': str(user_id)
        }
        return str(channel_id) == self.db_connection.fetch_single_data(query, params)

    def check_step_order(self, user_id):
        query = """
            SELECT progress_id
            FROM intro_task
            WHERE user_id = :user_id;
        """
        params = {
            'user_id': str(user_id)
        }
        return self.db_connection.fetch_single_data(query, params)

    def fetch_task_message_id(self, user_id: int) -> int:
        query = """
            SELECT task_message_id FROM karma_activity_log WHERE user_id = :user_id and task_id = (SELECT id FROM task_list WHERE hashtag = :hashtag)
            AND peer_approved = TRUE;
        """
        params = {
            'user_id': str(user_id),
            'hashtag': '#my-muid'
        }
        return self.db_connection.fetch_single_data(query, params)

    def check_muid(self, discord_id: int,muid) -> bool:
        query = """
            SELECT TRUE FROM user WHERE discord_id = :discord_id AND mu_id = :muid;
        """
        params = {
            'discord_id': str(discord_id),
            'muid': str(muid)
        }
        return self.db_connection.fetch_single_data(query, params)

    def update_order(self, user_id, progress):
        query = """
            UPDATE intro_task
            SET progress_id = :progress_id
            WHERE user_id = :user_id;
        """
        params = {
            'user_id': str(user_id),
            'progress_id': str(progress)
        }
        self.db_connection.execute(query, params)


    def update_progress(self,user_id: int, progress: int) -> None:
        query = """
            UPDATE intro_task SET progress_id = :progress_id, updated_by = :user_id WHERE user_id = :user_id;
        """
        params = {
            'user_id': str(user_id),
            'progress_id': progress
        }
        self.db_connection.execute(query, params)

    def fetch_muid(self, discord_id: int) -> str:
        query = """
            SELECT mu_id FROM user WHERE discord_id = :discord_id;
        """
        params = {
            'discord_id': str(discord_id)
        }
        return self.db_connection.fetch_single_data(query, params)

    def delete_log(self, discord_id: int) -> None:
        query = """
            DELETE FROM intro_task WHERE user_id = (SELECT id FROM user WHERE discord_id = :discord_id);
        """
        params = {
            'discord_id': str(discord_id)
        }
        self.db_connection.execute(query, params)