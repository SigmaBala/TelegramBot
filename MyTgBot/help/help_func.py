from telegraph import upload_file

async def grap(path):
     try:
         grap = upload_file(path)
         for id in grap:
              url = f"https://graph.org{id}"
     except:
          return False
     return url
