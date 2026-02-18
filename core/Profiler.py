import os
import json
from pathlib import Path
from terminaltables import SingleTable

class Profiler:
    """Manages OSINT profile persistence and database searching."""

    def export_text(self, file_name, path, data):
        """Safely exports raw text data to a file."""
        try:
            # Pathlib handles slashes automatically for Linux/Windows
            full_path = Path(path) / file_name
            full_path.write_text(data, encoding='utf-8')
            return True
        except Exception:
            return False

    def read_profile(self, file_name, path):
        """Reads and parses a .prfl JSON file."""
        p = Path(path)
        if not file_name.endswith('.prfl'):
            file_name = f"{file_name.replace(' ', '_')}.prfl"
        
        file_path = p / file_name
        try:
            if file_path.exists():
                return json.loads(file_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return None

    def write_profile(self, file_name, path, info):
        """Writes or updates a profile JSON file."""
        if not file_name.endswith('.prfl'):
            file_name = f"{file_name.replace(' ', '_')}.prfl"
        
        file_path = Path(path) / file_name
        data_prfl = {}

        # Read existing data if it exists
        if file_path.exists():
            try:
                data_prfl = json.loads(file_path.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                pass

        # Update and Save
        data_prfl.update(info)
        try:
            file_path.write_text(json.dumps(data_prfl, indent=4), encoding='utf-8')
            return True
        except Exception:
            return False

    def load_database(self, path):
        """Indexes all .prfl files in a directory."""
        p = Path(path)
        # Using a dictionary comprehension for speed
        profiles = {f.name: i+1 for i, f in enumerate(p.glob("*.prfl"))}
        
        self.database = profiles
        self.count = len(profiles)
        # Size in KB
        self.size = sum(f.stat().st_size for f in p.glob("*.prfl")) / 1024

    # Backwards-compatible camelCase wrappers
    def loadDatabase(self, path):
        return self.load_database(path)

    def time_sort(self, data_list, reverse=False):
        """Sorts profile data by timestamp key."""
        merged = {}
        for dico in data_list:
            for timestamp, value in dico.items():
                # Handle duplicate timestamps by incrementing slightly
                ts = int(timestamp)
                while ts in merged:
                    ts += 1
                merged[ts] = value
        
        # Sort using Python's highly optimized Timsort
        sorted_keys = sorted(merged.keys(), reverse=reverse)
        return {k: merged[k] for k in sorted_keys}

    def show_all_profiles(self):
        """Displays all indexed profiles in a table."""
        if not hasattr(self, 'database'):
            print("[!] Database not loaded.")
            return

        table_data = [('ID', 'Name')]
        for filename, id_num in self.database.items():
            clean_name = filename.replace("_", " ").replace(".prfl", "")
            table_data.append((str(id_num), clean_name))

        print(SingleTable(table_data, " Database ").table)

    def showAllProfiles(self, database=None):
        if database is not None:
            # Accept an external database mapping
            table_data = [('ID', 'Name')]
            for filename, id_num in database.items():
                clean_name = filename.replace("_", " ").replace(".prfl", "")
                table_data.append((str(id_num), clean_name))
            print(SingleTable(table_data, " Database ").table)
            return
        return self.show_all_profiles()

    def search_database(self, query):
        """Searches for a profile by ID or Name."""
        if not hasattr(self, 'database'): return None

        # 1. Search by ID
        if query.isdigit():
            id_query = int(query)
            for filename, id_num in self.database.items():
                if id_num == id_query:
                    name = filename.replace("_", " ").replace(".prfl", "")
                    return {'id': id_num, 'name': name, 'file': filename}
            return None

        # 2. Search by Name
        # Format name to file standard: "john doe" -> "John_Doe.prfl"
        formatted_name = "_".join([n.capitalize() for n in query.split()]) + ".prfl"
        
        id_num = self.database.get(formatted_name)
        if id_num:
            name = formatted_name.replace("_", " ").replace(".prfl", "")
            return {'id': id_num, 'name': name, 'file': formatted_name}
        
        return None

    def searchDatabase(self, query, database=None):
        # If a database is provided, use it temporarily
        if database is not None:
            # emulate the same behavior using provided mapping
            if query.isdigit():
                id_query = int(query)
                for filename, id_num in database.items():
                    if id_num == id_query:
                        name = filename.replace("_", " ").replace(".prfl", "")
                        return {'id': id_num, 'name': name, 'file': filename}
                return None

            formatted_name = "_".join([n.capitalize() for n in query.split()]) + ".prfl"
            id_num = database.get(formatted_name)
            if id_num:
                name = formatted_name.replace("_", " ").replace(".prfl", "")
                return {'id': id_num, 'name': name, 'file': formatted_name}
            return None

        return self.search_database(query)

    def writeProfile(self, fileName, path, info):
        return self.write_profile(fileName, path, info)