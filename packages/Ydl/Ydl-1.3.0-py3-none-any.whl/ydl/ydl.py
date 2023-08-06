import youtube_dl
import os
import urllib.error
import urllib.request


class YouTube_Download:
    def __init__(self, url):
        self.url = url
        self.downloadable_url = []
        self.downloadable_ext = []
        self.downloadable_format = []
        self.downloadable_format_exp = []
        self.entities = {}
        try:
            with youtube_dl.YoutubeDL() as ydl:
                self.result = ydl.extract_info(url, download=False)
        except youtube_dl.utils.DownloadError as e:
            print(e)
            os._exit(0)
        if "entries" in self.result:
            video = self.result["entries"][0]
        else:
            video = self.result
        for i in video["formats"]:
            self.downloadable_url.append(i["url"])
            self.downloadable_ext.append(i["ext"])
            self.downloadable_format.append(i["format_id"])
            self.downloadable_format_exp.append(i["format"])
        self.entities['title'] = self.result['title']
        self.entities['uploader'] = self.result['uploader']
        self.entities['upload_date'] = self.result['upload_date']
        self.entities['view_count'] = self.result['view_count']
        self.entities['thumbnail'] = self.result['thumbnail']

    def get_url(self, itag):
        try:

            format_index = self.downloadable_format.index(str(itag))
            url = self.downloadable_url[format_index]
            return url
        except:
            return ""

    def download_file(self, url, dst_path):
        try:
            with urllib.request.urlopen(url) as web_file:
                data = web_file.read()
                with open(dst_path, mode="wb") as local_file:
                    local_file.write(data)
        except urllib.error.URLError as e:
            raise Exception("Download_Error")

    def ydl(self, itag, path):
        url = self.get_url(itag)
        ext_index = self.downloadable_format.index(str(itag))
        ext = self.downloadable_ext[ext_index]
        self.download_file(url, path + "." + ext)

    def downloadable(self):
        exp_list = []
        for ext, id in zip(self.downloadable_ext,
                           self.downloadable_format_exp):
            exp = str(id) + "(" + ext + ")"
            exp_list.append(exp)
        return exp_list

    def get_ext(self, itag):
        ext_index = self.downloadable_format.index(str(itag))
        ext = self.downloadable_ext[ext_index]
        return ext
