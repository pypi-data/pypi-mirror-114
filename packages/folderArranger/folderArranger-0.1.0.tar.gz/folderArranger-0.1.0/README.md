# folderArranger

This is a small library aimed at graders in engineering fields. Sometimes we have the problem that students use different forms to submit their projects. Some submit it in a zip file, some might submit it in a folder, some even submit it in a folder inside a zip file. They might have some additional unnecessary folders or files in their submissions which are to be deleted before a plagiarism check is applied. 

This library can help you with that. It is assumed that there is a root folder that contains all the projects belnging to different students. You can unzip zip files, move the contents up if there is a single folder in a students submission, you can check all extensions of all files, you can check files with specific extensions, you can remove files by name or by extensions, last but not least you can remove any non-English characters in the names of the folders and the files. This function also helps to organize the name of the folders given by Moodle into more readable formats.

Folders normally do not have an extension, in this package they are assigned an extension "FOLDER". **Do not forget to include a . to the beginning of extensions.**
