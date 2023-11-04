import os
import shutil
import openai
import logging

# Configure logging
logger = logging.getLogger('FileOperationsModule')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class FileOperationsModule:
    def __init__(self, current_directory):
        self.current_directory = current_directory

    def change_directory(self, directory_path):
        """
        Change the current working directory.

        Args:
            directory_path (str): The path to the new directory.

        Returns:
            str: Feedback or assistance provided for the change.
        """
        try:
            os.chdir(directory_path)
            self.current_directory = os.getcwd()
            return f"Changed directory to {self.current_directory}"
        except Exception as e:
            error_message = str(e)
            assistance = self.get_assistance(error_message)
            logger.error(f"Error: {error_message}\nAssistance: {assistance}")
            return assistance

    def list_files_and_directories(self):
        """
        List files and directories in the current directory.

        Returns:
            list: List of strings representing filenames and directory names.
        """
        items = os.listdir(self.current_directory)
        return items

    def create_directory(self, directory_name):
        """
        Create a new directory in the current directory.

        Args:
            directory_name (str): The name of the new directory.

        Returns:
            str: Feedback or assistance provided for the creation.
        """
        try:
            os.mkdir(os.path.join(self.current_directory, directory_name))
            return f"Created directory '{directory_name}' in {self.current_directory}"
        except Exception as e:
            error_message = str(e)
            assistance = self.get_assistance(error_message)
            logger.error(f"Error: {error_message}\nAssistance: {assistance}")
            return assistance

    def delete_file_or_directory(self, name):
        """
        Delete a file or directory.

        Args:
            name (str): The name of the file or directory to delete.

        Returns:
            str: Feedback or assistance provided for the deletion.
        """
        path = os.path.join(self.current_directory, name)
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"Deleted file '{name}'"
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return f"Deleted directory '{name}' and its contents"
            else:
                return f"Cannot delete '{name}' as it does not exist"
        except Exception as e:
            error_message = str(e)
            assistance = self.get_assistance(error_message)
            logger.error(f"Error: {error_message}\nAssistance: {assistance}")
            return assistance

    def get_assistance(self, context):
        """
        Get assistance from ChatGPT-3.5 for handling errors.

        Args:
            context (str): The context or error message.

        Returns:
            str: Assistance provided by ChatGPT-3.5.
        """
        openai.api_key = 'your-api-key'
        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=f"I encountered an error: {context}. How should I proceed?",
                max_tokens=100
            )
            assistance = response.choices[0].text.strip()
            return assistance
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error getting assistance: {error_message}")
            return "I encountered an error and couldn't get assistance."

# Example usage:
if __name__ == "__main__":
    current_directory = os.getcwd()
    file_ops = FileOperationsModule(current_directory)

    print(file_ops.change_directory("/path/to/directory"))
    print(file_ops.list_files_and_directories())
    print(file_ops.create_directory("new_directory"))
    print(file_ops.delete_file_or_directory("file.txt"))
