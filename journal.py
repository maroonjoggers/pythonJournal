import argparse
import json
import os.path
from datetime import date

class journal(object):

    def __init__(self):
        super(journal, self).__init__()
        self.args = self.get_args()

        self.user = self.args.username

        #if file with username already exists, then do somehting
        self.file = "journal" + self.user + ".json"

        # Debug this
        # if os.path.isfile(self.file):
        #     print("This user exists, would you like to write to this user's journal? (Y/N)")
        #     s = input().upper()
        #     if s != "Y" and s != "N":
        #         print("Invalid input")
        #         exit()
        #     elif s == "N":
        #         exit()
        #     elif s == "Y":
        #         print("Adding entry...")

        self.find_file()

        if self.args.title and not self.title_exists():
            self.title = self.args.title
        else:
            self.title = ''

        self.entry = self.args.create if self.args.create else ''

        # Can implement adding user id here potentially


        # if theres a list command in my args
        if self.args.list:
            self.get_titles()

        # if theres a delete command in my args
        if self.args.delete_entry:
            self.delete_entry(self.args.delete_entry)

        if self.args.delete_user:
            self.delete_user()

        if self.args.sort:
            self.sort(self.args.sort)

    def find_file(self):
        if not os.path.isfile(self.file):
            with open(self.file, "w+") as journal_file:
                journal = {}
                journal_file.write(json.dumps(journal))

    def get_args(self):
        parser = argparse.ArgumentParser(description="Add entries to your journal!")

        parser.add_argument(
            'username',
            type=str,
            help="Username of user's journal"
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help="Print list of titles"
        )
        parser.add_argument(
            '--delete_entry',
            type=str,
            help="Delete an entry with a certain title"
        )
        parser.add_argument(
            '--delete_user',
            #type=str,
            action='store_true',
            help="Delete a user's journal"
        )
        parser.add_argument(
            '--create',
            type=str,
            help="Contents of a new journal entry"
        )
        parser.add_argument(
            '--title',
            type=str,
            help="Title of entry"
        )
        parser.add_argument(
            '--sort',
            type=str,
            help="Print out sorted entries (ascending/descending)"
        )

        args = parser.parse_args()
        return args

    def write(self, title, entry, date=date.today().isoformat()):
        with open(self.file, "r") as journalFile:
            journal = json.load(journalFile)

        with open(self.file, "w+") as journalFile:
            entry = {"date": date, "Title": title, "Entry": entry}
            # Sorting for a clean json file
            entryNum = int(sorted(journal.keys())[-1]) + 1 if len(journal.keys()) > 0 else 1
            journal[str(entryNum)] = entry
            journalFile.write(json.dumps(journal, ensure_ascii=True, indent=4))
            print("Successfully added your entry")

    def sort(self, order):
        if order != "ascending" and order != "descending":
            print("Invalid input")
            exit()

        with open(self.file) as json_file:
            data = json.load(json_file)

        entries = list(data.values())


        if order == "ascending": # Oldest to newest
            entries = sorted(entries, key=lambda k: k["Title"])

        for e in entries:
            print(e["Title"])
        #
        # elif order == "descending": # Newest to oldest
        #     data = sorted(data, key=lambda k: k["Title"], reversed = True)
        # print(entries[""])



    def get_titles(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
        titles = []
        for i in data:
            titles.append(data[i]['Title'])
        print(titles)

    def title_exists(self):
        with open(self.file) as json_file:
            data = json.load(json_file)
        for i in data:
            if data[i]['Title'] == self.args.title:
                print("Already have an entry with this title, Would you like to edit (Y/N)?")
                s = input().upper()
                self.edit(s)
                return True
        return False

    def edit(self, s):
        if s != "Y" and s != "N":
            print("Invalid input")
        elif s == "Y":
            print("Enter your new entry: ")
            new_entry = input() # Ensure this is a string or cast it to one
            with open(self.file) as json_file:
                data = json.load(json_file)
            for i in data:
                if data[i]['Title'] == self.args.title:
                    data[i]['Entry'] = new_entry
                    print("Entry updated")

            with open(self.file, 'w') as data_file:
                json.dump(data, data_file, ensure_ascii=True, indent=4)



    def delete_entry(self, to_remove):
        with open(self.file) as json_file:
            data = json.load(json_file)

        indices = []
        for i in data:
            if data[i]['Title'] == to_remove:
                indices.append(i)

        if len(indices) == 0:
            print("No entry with that title exists")
            return

        for i in indices:
            del data[i]
        print("Deleted entry with title: " + to_remove)

        with open(self.file, 'w') as data_file:
            json.dump(data, data_file, ensure_ascii=True, indent=4)
            #Check indices

    def delete_user(self):
        #Check user exists
        #Write logic to delete self.file
        if os.path.exists(self.file):
            os.remove(self.file)
        else:
            print("Can not delete the user as it doesn't exists")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Maybe add check for duplicate titles?
    journal = journal()
    if journal.title and journal.entry:
        journal.write(journal.title, journal.entry)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
