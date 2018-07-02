class PDFData:
    def __init__(self):
        self.name="pdf_data"
        self.runonce=False
    def parse_page(self,page_data,page_url):
        if(page_url[-4:]==".pdf"):
            return {"source":page_url}
        else:
            return {}
module=PDFData()
