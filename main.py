import os
import pathlib

import requests
from bs4 import BeautifulSoup

urls = [
    'https://www.mongard.ir/courses/regex-course/',
]


def main():
    s = requests.Session()
    login_p = s.get('https://www.mongard.ir/accounts/login/')
    login_soup = BeautifulSoup(login_p.text, 'html.parser')
    hiddens = login_soup.select('input[type=hidden]')
    data = {hidden.get('name'): hidden.get('value') for hidden in hiddens}
    data.update({'email': 'amirex128@gmail.com', 'password': 'a6766581'})
    s.post('https://www.mongard.ir/accounts/login/', data=data)
    for url in urls:
        course = s.get(url)
        home_course = 'videos/' + url.split('/')[-2]
        print(f'\r course : {home_course}')
        soup = BeautifulSoup(course.text, 'html.parser')
        episodes = soup.select('.episode_container:not(:first-child)')
        for episode in episodes:
            href = episode.select('a.episode_link')[0].attrs['href']
            number = episode.select('.episode_counter')[0].text
            name_file = episode.select('a.episode_link > h3')[0].text
            print(f'\r{number} {name_file}')
            page_video = s.get('https://www.mongard.ir' + href)
            soup_video = BeautifulSoup(page_video.text, 'html.parser')
            link_download = soup_video.select('.video_download_container > p > a')[0].attrs['href']
            res_download = s.get(link_download, stream=True)
            pathlib.Path(f'{pathlib.Path(__file__).parent.resolve()}/{home_course}').mkdir(parents=True, exist_ok=True)
            path_file=f'{pathlib.Path(__file__).parent.resolve()}/{home_course}/{number}_{name_file.replace("/","")}.mp4'
            if os.path.exists(path_file):
                print(f'\r{number} {name_file} exist')
                continue
            with open(path_file, 'wb') as f:
                download = 0
                total = int(res_download.headers.get('content-length', 0))
                for chunk in res_download.iter_content(chunk_size=1024):
                    if chunk:
                        download += len(chunk)
                        done = int(50 * download / total)
                        print(
                            f'\r{done * "="}>{(50 - done) * " "} {download / 1024 / 1024:.2f}MB/{total / 1024 / 1024:.2f}MB',
                            end='')
                        f.write(chunk)


if __name__ == '__main__':
    main()
