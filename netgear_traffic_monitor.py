from pynetgear import Netgear
import json
import time
import queue

ROUTER_ADMIN_PASSWORD = 'router_admin_password'
NEW_TODAY_UPLOAD = 'NewTodayUpload'
NEW_TODAY_DOWNLOAD = 'NewTodayDownload'

def get_router_admin_password():
    with open('config.json') as config_json:
        config = json.load(config_json)
        return config[ROUTER_ADMIN_PASSWORD]

def get_traffic_json(netgear):
    traffic = netgear.get_traffic_meter()
    traffic_json = json.dumps(traffic)
    traffic_json = json.loads(traffic_json)
    return traffic_json

def get_today_upload_and_download(netgear):
    traffic_json = get_traffic_json(netgear)
    new_today_upload = traffic_json[NEW_TODAY_UPLOAD]
    new_today_download = traffic_json[NEW_TODAY_DOWNLOAD]
    return new_today_upload, new_today_download

def main():
    netgear = Netgear(password=get_router_admin_password())
    upload_queue = queue.Queue()
    download_queue = queue.Queue()

    cumulative_upload = 0
    cumulative_download = 0
    duration = 1
    init_upload, init_download = get_today_upload_and_download(netgear)
    upload_queue.put(init_upload)
    download_queue.put(init_download)

    while True:
        time.sleep(1)
        new_upload, new_download = get_today_upload_and_download(netgear)
        upload_queue.put(new_upload)
        download_queue.put(new_download)
        if duration < 10:
            duration += 1
        else:
            init_upload = upload_queue.get()
            init_download = download_queue.get()

        upload_rate = (new_upload - init_upload) / duration
        download_rate = (new_download - init_download) / duration

        print("Upload Rate: ", '%.3f' % (upload_rate * 1024),"KB,\tDownload Rate: ", '%.3f' % (download_rate), "MB")


#for i in netgear.get_attached_devices():
#    print(i)


if __name__ == "__main__":
    main()

