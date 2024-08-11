import os
import shutil

# Define the source directory
src_dir = r"C:\dev\Assistant\src\backend\components"
# Define the target directories
target_dirs = {
    "google_calendar": r"C:\dev\Assistant\src\backend\components\Google\Calendar",
    "google_drive": r"C:\dev\Assistant\src\backend\components\Google\Drive",
    "google_gmail": r"C:\dev\Assistant\src\backend\components\Google\Gmail",
    "google_tasks": r"C:\dev\Assistant\src\backend\components\Google\Tasks",
    "google_youtube": r"C:\dev\Assistant\src\backend\components\Google\Youtube"
}

# Define the files to rename and move
files_to_move = {
    "AddItemToYoutubePlaylist.py": ("youtube_playlist_add_item.py", target_dirs["google_youtube"]),
    "CreateGoogleCalendarEvent.py": ("google_calendar_event_create.py", target_dirs["google_calendar"]),
    "CreateGoogleCredentials.py": ("google_credentials_create.py", target_dirs["google_drive"]),
    "CreateGoogleTask.py": ("google_task_create.py", target_dirs["google_tasks"]),
    "CreateYoutubePlaylist.py": ("youtube_playlist_create.py", target_dirs["google_youtube"]),
    "DeleteFile.py": ("file_delete.py", src_dir),  # Remains in components
    "ExampleTool.py": ("utility_example_tool.py", src_dir),  # Remains in components
    "GetAndParseEmail.py": ("email_get_and_parse.py", target_dirs["google_gmail"]),
    "GetTimeAndDate.py": ("time_and_date_get.py", src_dir),  # Remains in components
    "GoogleSearch.py": ("search_google.py", src_dir),  # Remains in components
    "ListFiles.py": ("file_list.py", src_dir),  # Remains in components
    "ListGoogleCalendarEvents.py": ("google_calendar_events_list.py", target_dirs["google_calendar"]),
    "ListGoogleEmails.py": ("email_list_google.py", target_dirs["google_gmail"]),
    "ListGoogleTasks.py": ("google_tasks_list.py", target_dirs["google_tasks"]),
    "ListYoutubePlaylists.py": ("youtube_playlist_list.py", target_dirs["google_youtube"]),
    "ParseWebsite.py": ("website_parse.py", src_dir),  # Remains in components
    "ReadFile.py": ("file_read.py", src_dir),  # Remains in components
    "SaveImportantInfo.py": ("info_save_important.py", src_dir),  # Remains in components
    "SearchYoutubeVideo.py": ("youtube_video_search.py", target_dirs["google_youtube"]),
    "WriteFile.py": ("file_write.py", src_dir)  # Remains in components
}

# Iterate through the files to rename and move
for old_filename, (new_filename, target_dir) in files_to_move.items():
    old_file_path = os.path.join(src_dir, old_filename)
    new_file_path = os.path.join(target_dir, new_filename)

    # Rename and move the file
    try:
        shutil.move(old_file_path, new_file_path)
        print(f"Renamed and moved: {old_filename} -> {new_filename}")
    except FileNotFoundError:
        print(f"File not found: {old_filename}")
    except Exception as e:
        print(f"Error moving {old_filename}: {e}")

print("File renaming and moving completed.")