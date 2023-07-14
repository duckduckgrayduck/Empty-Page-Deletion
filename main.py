"""
This DocumentCloud Add-On searches through each page in a document 
and if that page does not have underlying text, and the user has selected to delete it, 
the empty pages will be deleted. 
"""

from documentcloud.addon import AddOn
import fitz 
import os

class PageDeleter(AddOn):
    """DocumentCloud Add-On that detects empty pages and deletes them."""

    def main(self):
        os.makedirs(os.path.dirname("./out/"), exist_ok=True)
        to_include=[]
        access_level = self.data["access_level"]
        project_id = self.data.get("project_id")
        for document in self.get_documents():
            title = document.title
            with open(f"{title}.pdf", "wb") as file:
                file.write(document.pdf)
            input_file = f"{document.title}.pdf"
            output_file = f"./out/{document.title}-clean.pdf"
            file_handle = fitz.open(input_file)
            for page in range(1,document.pages+1):
                if document.get_page_text(page).isspace() or document.get_page_text(page)=="" or document.get_page_text(page).rstrip()=='.':
                   print(f"{page}")
                else:
                    to_include.append(page-1)
            file_handle.select(to_include)
            file_handle.save(output_file)
        obj_list = self.client.documents.upload_directory("./out/")
        project = self.client.projects.get(project_id)
        project.document_list = obj_list
        project.put()

if __name__ == "__main__":
    PageDeleter().main()
