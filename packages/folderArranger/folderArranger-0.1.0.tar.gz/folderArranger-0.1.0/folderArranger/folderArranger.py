import os
import zipfile
import unicodedata
from colorama import init as colorama_init
from colorama import Fore

colorama_init(autoreset=True)


class FolderArranger:
    def __init__(self, root_path, verbose=True):
        self.root_path = root_path
        os.chdir(root_path)

        root_folder_names = os.listdir()
        problem_flag = all(list(map(os.path.isdir, root_folder_names)))
        if not problem_flag:
            raise Exception('The root folder should contain only folders')

        self.verbose = verbose

    def move_single_folders_up(self):
        folder_names = os.listdir()
        for folder_name in folder_names:
            curr_contents = os.listdir(folder_name)
            if len(curr_contents) == 1:
                only_content_name = curr_contents[0]
                path_to_content = os.path.join(folder_name, only_content_name)
                directory_flag = os.path.isdir(path_to_content)
                if directory_flag:
                    os.system(f'move "{path_to_content}\\*" "{folder_name}" 1>nul')
                    os.rmdir(path_to_content)
                    if self.verbose:
                        print(f'{folder_name} had only a single folder in it and all the content is moved up.')

    def unzip_single_zips(self):
        folder_names = os.listdir()
        for folder_name in folder_names:
            curr_contents = os.listdir(folder_name)
            if len(curr_contents) == 1:
                only_content_name = curr_contents[0]
                curr_extension = os.path.splitext(only_content_name)[1]
                if curr_extension == '.zip':
                    try:
                        path_to_zip_file = os.path.join(folder_name, only_content_name)
                        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_handle:
                            zip_handle.extractall(folder_name)
                        os.remove(path_to_zip_file)
                        if self.verbose:
                            print(f'{folder_name} had only one single zip file and it has been extracted.')
                    except zipfile.BadZipfile:
                        print(Fore.RED + f'{folder_name} had only one single zip but it could NOT be extracted. You might need to extract that manually.')

    def unrar_single_rars(self):
        unrar_exe_path = os.path.dirname(os.path.abspath(__file__))
        unrar_exe_path = os.path.join(unrar_exe_path, 'UnRAR.exe')

        if not os.path.exists(unrar_exe_path):
            raise Exception('You need the UnRAR.exe to be able to unrar stuff!')

        folder_names = os.listdir()
        for folder_name in folder_names:
            curr_contents = os.listdir(folder_name)
            if len(curr_contents) == 1:
                only_content_name = curr_contents[0]
                curr_extension = os.path.splitext(only_content_name)[1]
                if curr_extension == '.rar':
                    try:
                        path_to_rar_file = os.path.join(folder_name, only_content_name)
                        os.system(f'{unrar_exe_path} x "{path_to_rar_file}" "{folder_name}" 1>nul')
                        os.remove(path_to_rar_file)
                        if self.verbose:
                            print(f'{folder_name} had only one single rar file and it has been extracted.')
                    except:
                        print(Fore.RED + f'{folder_name} had only one single rar but it could NOT be extracted. You might need to extract that manually.')

    def check_extensions(self):
        all_used_extensions = set()
        folder_names = os.listdir()
        for folder_name in folder_names:
            curr_contents = os.listdir(folder_name)
            for curr_content in curr_contents:
                curr_extension = os.path.splitext(curr_content)[1]
                if curr_extension == '':
                    curr_path = os.path.join(folder_name, curr_content)
                    if os.path.isdir(curr_path):
                        all_used_extensions.add('FOLDER')
                    else:
                        all_used_extensions.add(curr_extension)
                else:
                    all_used_extensions.add(curr_extension)
        return all_used_extensions

    def check_files_with_extension(self, extension):
        assert isinstance(extension, str), Fore.RED + f'extension should be a string. Instead you used {extension}'
        if extension in self.check_extensions():
            if extension != 'FOLDER' and extension != '':
                folder_names = os.listdir()
                for folder_name in folder_names:
                    curr_contents = os.listdir(folder_name)
                    for curr_content in curr_contents:
                        curr_extension = os.path.splitext(curr_content)[1]
                        if curr_extension == extension:
                            file_path = os.path.join(folder_name, curr_content)
                            print(f'A file with extension {extension} is {file_path} ')

            elif extension == '':
                folder_names = os.listdir()
                for folder_name in folder_names:
                    curr_contents = os.listdir(folder_name)
                    for curr_content in curr_contents:
                        curr_extension = os.path.splitext(curr_content)[1]
                        curr_path = os.path.join(folder_name, curr_content)
                        not_dir_flag = not os.path.isdir(curr_path)
                        if curr_extension == extension and not_dir_flag:
                            file_path = os.path.join(folder_name, curr_content)
                            print(f'A file with extension {extension} is {file_path} ')

            else:
                folder_names = os.listdir()
                for folder_name in folder_names:
                    curr_contents = os.listdir(folder_name)
                    for curr_content in curr_contents:
                        file_path = os.path.join(folder_name, curr_content)
                        if os.path.isdir(file_path):
                            print(f'A file with extension {extension} is {file_path} ')
        else:
            print(Fore.RED + f'There are no files with the extension {extension}')

    def remove_file(self, file_name):
        assert isinstance(file_name, str), Fore.RED + f'file_name should be a string. Instead you used {file_name}'
        found_flag = False
        folder_names = os.listdir()
        for folder_name in folder_names:
            curr_contents = os.listdir(folder_name)
            if file_name in curr_contents:
                file_path = os.path.join(folder_name, file_name)
                os.remove(file_path)
                print(f'{file_path} is deleted.')
                found_flag = True

        if not found_flag:
            print(Fore.RED + f'There are no files with the name {file_name}. Do not forget to include the extension in the file name as well if you did not.')

    def remove_files(self, file_names):
        assert isinstance(file_names, list), Fore.RED + f'file_names should be a list.'
        for file_name in file_names:
            self.remove_file(file_name)

    def remove_files_with_extension(self, extension):
        assert isinstance(extension, str), Fore.RED + f'extension should be a string. Instead you used {extension}'
        if extension in self.check_extensions():
            folder_names = os.listdir()
            for folder_name in folder_names:
                curr_contents = os.listdir(folder_name)
                curr_extensions = [os.path.splitext(curr_content)[1] for curr_content in curr_contents]
                if extension in curr_extensions:
                    for curr_content in curr_contents:
                        curr_extension = os.path.splitext(curr_content)[1]
                        if curr_extension == extension:
                            file_path = os.path.join(folder_name, curr_content)
                            os.remove(file_path)
                            print(f'{file_path} is deleted.')
        else:
            print(Fore.RED + f'There are no files with the extension {extension}')

    def verify_folder_composition(self, desired_extensions):
        assert isinstance(desired_extensions, list), f'desired extensions should be a list'
        desired_extensions.sort()

        bad_folders = []

        if 'FOLDER' not in desired_extensions:
            folder_names = os.listdir()
            for folder_name in folder_names:
                curr_contents = os.listdir(folder_name)
                curr_extensions = [os.path.splitext(curr_content)[1] for curr_content in curr_contents]
                curr_extensions.sort()
                if not curr_extensions == desired_extensions:
                    bad_folders.append(folder_name)
        else:
            folder_names = os.listdir()
            for folder_name in folder_names:
                curr_extensions = []
                curr_contents = os.listdir(folder_name)
                for curr_content in curr_contents:
                    curr_path = os.path.join(folder_name, curr_content)
                    if os.path.isdir(curr_path):
                        curr_extensions.append('FOLDER')
                    else:
                        curr_extension = os.path.splitext(curr_content)[1]
                        curr_extensions.append(curr_extension)

                curr_extensions.sort()
                if not curr_extensions == desired_extensions:
                    bad_folders.append(folder_name)

        print(Fore.BLUE + f'Here is a list of bad folders:')
        for bad_folder in bad_folders:
            print(bad_folder)

    def beautify_bad_names(self):
        folder_names = os.listdir()
        for folder_name in folder_names:
            student_name = folder_name.split('_')[0]  # Because of Moodle names
            temp_names = student_name.split()
            temp_names = [
                unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf8').lower().capitalize() for
                name in temp_names]
            temp_names = temp_names[-1:] + temp_names[:-1]  # I want to have the last name at the beginning
            new_folder_name = ''.join(temp_names)
            for content_name in os.listdir(folder_name):
                new_content_name = unicodedata.normalize('NFKD', content_name).encode('ascii', 'ignore').decode('utf8')
                new_content_name = ''.join(new_content_name.split())
                new_content_path = os.path.join(folder_name, new_content_name)
                old_content_path = os.path.join(folder_name, content_name)
                os.rename(old_content_path, new_content_path)
                if new_content_path != old_content_path and self.verbose:
                    print(f'Renaming {old_content_path} to {new_content_path}')
            os.rename(folder_name, new_folder_name)
            if new_folder_name != folder_name and self.verbose:
                print(f'Renaming {folder_name} to {new_folder_name}')


