# NAY XAI TU 15 - 17
import uuid
from multiprocessing import Process, Queue
import os
import time
import subprocess

CURRENT_EXEC_PATH = os.getcwd()
BUCKET_NAME = 'ty-bucket-farm-22'
RUN_CONFIG = [{'id': 'a3b281d1-5361-420d-b5fb-99c8bd888f35', 'share_drive_id': '0AH_MimWfwAeXUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_M05-iqll3Idh8trXG_SGtYE1e7U3zc2OIwRm8P5-IhGF2lLN2wxB4KuwaChfbTmtdNGZLR0GF63B9C2ts2iD5oDyF61DtnUHgAkGLt9Vt2pQq4BLdCe1uVGdomb5JV771s_Vy_3KgTdGTIbmjFweG","token_type":"Bearer","refresh_token":"1//0e7keAsyNiE21CgYIARAAGA4SNwF-L9IrPEh9wVD8iVE8u9v14Wky1BjLOsjX7RE7KefT8C69tAanZBKF1rJYDDLiHmDibQVWGu8","expiry":"2021-08-18T14:04:52.2720643+07:00"}'}, {'id': '22d3fe5c-8c59-42c0-b97a-a1b26390bceb', 'share_drive_id': '0ANNYq_opTBVDUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM98tadXGlXQA9jQ3JCzVPXcSJk0qlDrurc7iswxHMUKZpNgQ3UJ1ajSa-jXfcAt5JmtyM6tZJ6rUMURDNykT-d3U7vVISuzHQu7GdGGkXBwYib1c4tu3nk9ySBRO22Jbe2VkduNSUs7g9lZ244skDWW","token_type":"Bearer","refresh_token":"1//0emImTAfriNIECgYIARAAGA4SNwF-L9IrizCoH-5rZtiPyjnK7J062Q0Roi8z4TAIJjUCQ3CegFkVa9YjeXBAjlzHPxvsAESAq34","expiry":"2021-08-18T14:05:50.3927271+07:00"}'}, {'id': 'da2bba62-e4b2-46c6-aa62-7cd579435356', 'share_drive_id': '0AKyo9K-0F2iZUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM85VErNuOBtDpOWZx4qG4LQx0MZA9Fer2mUjK_PxzZLaGBZRyGnc6W7XwnrYgELneS19LJ3kWlu4he9mMGpzIBsRpmkvFL3Sgrq9Mrq_7zaJoUj9UuNDqN_QvqULfaxMxKqjXNZuUlgr2qaAgQmC8LN","token_type":"Bearer","refresh_token":"1//0eDb11FHL8DCtCgYIARAAGA4SNwF-L9IrHYf_xsUCYpPsAi99P7i4hQpYnqqGjltxILe_o-gD0Uu8PWI9i9TXIADBLNll8rKgMnc","expiry":"2021-08-18T14:06:17.9415136+07:00"}'}, {'id': '4ca19cff-c11e-4b58-8b54-435491a24d59', 'share_drive_id': '0AGSUcB_qkWwqUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9tu709t5x5rpLEBBpJQPWj49fZsNuzP906ECKbnFHbmSu0kYWuKlJziPwBWHED3HXXv0Xk_pfYJPZJ7vOq5fHl8rPvS-TxnqeozQNo2rQ_6nJ4sMsdVo7bmigrcIYc-mrAD51mw8INaVLSjPY3Nhy9","token_type":"Bearer","refresh_token":"1//0eubJO7eO10zOCgYIARAAGA4SNwF-L9IrrleqXGmP7fC_amUVCMZoAdus0rDF3nXYsoirKM2CPM5xyDPbv5ekEUblorkrRyeXAMk","expiry":"2021-08-18T14:06:41.8943525+07:00"}'}, {'id': '546d7890-78c6-4168-b15c-ffc84383cd2b', 'share_drive_id': '0AJEHWDKHRZUyUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_TmG3jDtv_HhuRv-wMnzylP0Sc7pzo_KTzidz9CXYTHuXVoFawHra7FaHS1yp9mudynKQJNWSo5NNrmKQfRVA5DpM82oh5LW3uMQxMT1-vCek7xCqpIWMIkuCotQjhOrkjIt1FynyD6-ue3x-5twwn","token_type":"Bearer","refresh_token":"1//0e1c5wJ6H5DhkCgYIARAAGA4SNwF-L9IrQcFbUBmjYrkyIacnwx44WMPwvw9NV89S0R-_rbpe6BJxOhtq_VuTTlFETHfcXb5J9Yc","expiry":"2021-08-18T14:07:06.1655253+07:00"}'}, {'id': '796e9748-4a37-46af-8be7-ded5671e7941', 'share_drive_id': '0AEj8Ch0cX0yRUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_iPoc9zST3zFrAAqA6hothAeusb20qwSLhtkIkgKqNCdhI8UWN0YDB3C1AVqCbMbcieUISyJBwshuAPJu8kOjX28VWgjy-3VJwgV_ZXtaPjbiZNEGdGsBrgVVfrdzwgULZ45silabWfmFRoohQK5io","token_type":"Bearer","refresh_token":"1//0elaztZ4vkS26CgYIARAAGA4SNwF-L9Irk5bkDGSN8qdGRFznpIeEQXXTco-UWnbeMhcIR2CC9s5vIBUHSgOmfeRCb4rndHLenkY","expiry":"2021-08-18T14:08:11.5419379+07:00"}'}, {'id': '19333065-afd4-4ec2-9adf-121d0eaf7708', 'share_drive_id': '0AAkRcbZoZz_ZUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_-FtS1z8YSSoTfbJ9Trra0v2aBgAmbo_N1t7W6GHc7Awf2HzPHx68m5yi1b-1lc0xxfkixs3pQT2tkfxR1KIjCnKFVKJ1eX7Jh72eCJAUYtKsFqOCq53DeQqocM9kH_dsQsuXy4YkxayBUM78pkodB","token_type":"Bearer","refresh_token":"1//0e7v9Gm0aTh5wCgYIARAAGA4SNwF-L9Ir99XrCOzN2j9lISRSYEsDRMDSiB5VJ0yZPrm3ZkcvpFAfh2cAY7l8iJU4ECWYafy5Ph0","expiry":"2021-08-18T14:08:36.3854191+07:00"}'}, {'id': '29249b64-b30e-4c86-adff-5ce501cfb306', 'share_drive_id': '0ALaegGP8nqd5Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8EAkm7iTjQT6-N-_JjRKC3Z69GCZlvohM1ooQsuzRsZD_gC2_fXRPDrW4oKVM5kqu68-w0Jqmm9SUldhrIikbsQviudZDqkGY7QtbcLGHNFN-Eg39CIJHmNkPhVCSjtJnh3Yj3Fg0keSTjzXlDcpWS","token_type":"Bearer","refresh_token":"1//0eYwTvZcihS_VCgYIARAAGA4SNwF-L9IrQMEV0LtUp3Cz7cXXFOi9kdMrBj1qJiXJFLAwWC4MPQr7dWGBwA_Y9IWr2Fi9BbLgBY8","expiry":"2021-08-18T14:09:11.6548198+07:00"}'}, {'id': 'b40c8050-ac07-425b-b8b8-ee467c936222', 'share_drive_id': '0ALV-d0LoBQTiUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_S-9YmtSv6jTlIowRpgRs4x6D1jZnt1_Yb0aootqrnGUFxR848cnE9vV3c1Lt7D-SKK8_AfExVrJpJjxLH8R8qXw76EQJ4A2wSS7nXnxcjICB2Jmg3GA0XlXqMJYd3Cg9lC6i7GO2XrB5HihbnfvCB","token_type":"Bearer","refresh_token":"1//0ekXIRkEIaNCwCgYIARAAGA4SNwF-L9IrLPXDeoZv03gnFP2_o-olXIX6_UbF2KWDVJAVCeOJObD4_STkjeBJSEjZ81XehaY5ZgQ","expiry":"2021-08-18T14:09:43.6783757+07:00"}'}, {'id': '8a3629d1-7886-4335-9487-c403a47df1e3', 'share_drive_id': '0ANr4u8pcP05eUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9Gvs1PjDSLLb09DzvDOlt-V9SZ5exf-NV6zXpmKWbWeLWKhvt8fNMs7aUZOLdt7IpOMQW2jZcy3sIS-OkfQp9Ox89M7ImdksvGR9W2UnJFWxJZkWTgEzSHGp-mr3o8bkWk0nvF--zEAVoImPDgM513","token_type":"Bearer","refresh_token":"1//0e44degUO2MovCgYIARAAGA4SNwF-L9IrydvtmWKP8u6OOMp7kHmbJ52hXMMWKOtP_W34FskXYz3U-V7dHPy-iVZwBV3BKnk99hs","expiry":"2021-08-18T14:10:06.1790713+07:00"}'}, {'id': '6cc96724-b00d-42a7-83bd-ae7768dd93cb', 'share_drive_id': '0AM4sF6wfLLYdUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_LLmdQOdey5Gb2s2G1Ln5MCWOYgX0pn7F5oCnkW34sYQtItBExNV3tW4HtdvLHw565b2EB9cH9bJrqMt8VG2fcCVbl6V1Gr9fG6SAOgf7_EziR6Rj_HistGAvY6OSKtmhnKwm57at2PaCTepDMa4tT","token_type":"Bearer","refresh_token":"1//0eAehLomLv3Z4CgYIARAAGA4SNwF-L9IrwDvUJ2-IL9g3f5HOPOjaRxbnIz1m-JlVeGepIticddSDD3MtgIcPwzfc1L8sAcbA884","expiry":"2021-08-18T14:17:34.8704993+07:00"}'}, {'id': 'e687b00a-10f5-40e5-ad67-387bec4ba52a', 'share_drive_id': '0AGcZwQBgtR-SUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_jK1mAwcTPH4eDBeeYTWjMjGIlfNiAFYnJ5mIdK8nvdT7m6NE-bDTcODV3wvEil-leU3rT68TMnZZous6WwDACahDI7SKDhHq-qsRCMDXP9-Iq2TD8zpuCQ-ZpllpVd7JQPFcD64TWf7Q8EfJSsZz_","token_type":"Bearer","refresh_token":"1//0eHEvoSI0GuwsCgYIARAAGA4SNwF-L9IrzVTstH4qb5BN1R7JplJYNJ_KrzhBOh7cnRBhmEQs_PrtKfE9TjBcP4_pdk0UpMCFvMs","expiry":"2021-08-18T14:18:02.120876+07:00"}'}, {'id': 'f2428858-d361-4bd4-947d-5d31fafb07b6', 'share_drive_id': '0AIwjde3fZPNZUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM86lEsjC7NCsMt6jHEKOGmauIi5FVXBxuLnsRIk8Mw_0_k2-5wVFr0LpJChf1fGEaXZ4iW2-ABQHCeuKgdtxL2rn3MNb19q2jJvegzPi2KX8XuLrmHVUKW9c6CtliDeJxksKtzJXori3sE1M3Vj1sKk","token_type":"Bearer","refresh_token":"1//0eWi1ayt-7K2-CgYIARAAGA4SNwF-L9IrvTOztOdPmpgu34QvvvgPSFCqJRpzX17k6h8PQvUWE_nycDt-l7PCnhAGU_Ua_wf4B3A","expiry":"2021-08-18T14:18:32.0753091+07:00"}'}, {'id': 'b7c1688e-f561-413b-804c-68be317ecf49', 'share_drive_id': '0ACfSrtdx6ULNUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-MY2dUu8qynumI1kR3Kc30uOLbBmqu6m2OFiK3M5uvWd-YvQNfWlCIvYwCpiyws9zgA-xO1mqLDVkA6Gn0gLCaL-x6h1pi7uz_i_Zm8LD7rldFm3_F0L_BDntK23JRMXTAOxdcLMlMK2LSlZ6lYdTZ","token_type":"Bearer","refresh_token":"1//0eiuldKYpMjHcCgYIARAAGA4SNwF-L9IrtsYK3Gdt0yxwQrjJCT3OhOeYweZt2-NdEOs-ecu_iducM36RExRPdtVU6jH8zyT9PHQ","expiry":"2021-08-18T14:18:53.33193+07:00"}'}, {'id': '13c48035-2b01-48d1-9ba8-819af12cfb28', 'share_drive_id': '0AK7U1ZvYUDIIUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM--TN-Jjk64mtn6yJ4BnbRxuOR4P9dlYdV7zs1UU5o1caK68on6yh6iUYumq9XEDZj_BOjzcFUrt5NfNMJvzzCnmq84esx0ah1s9w97VU0FJc9LC2VI6kzq6RvU26JRA6hIYXMczBa7PRsD2WmZIhAy","token_type":"Bearer","refresh_token":"1//0esWLHZcAYmEuCgYIARAAGA4SNwF-L9IrS-Dr5JETd6Ncec8ixD0TLdRu4ebwfveg2mAhfIHu0gzCErjzPeDsXPJPFG2nj5axCS8","expiry":"2021-08-18T14:19:19.5777359+07:00"}'}, {'id': '23400917-feca-4810-b031-67c003f74932', 'share_drive_id': '0AIcdEX0ASKl3Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8C1Y8ZJzuEYePIeK1WnwnO8Xt0Lg25_apsnSLNjOCQk_VFX1i_hs5u19OCFlYDKvX5Bapvg2tlnvMWQsgkKdlmR-a6Zuv70-t6X-NkJPnl2bov5RWIXwLO54RIY1wJcMIqDPuZzOwqkY3osXia9YCF","token_type":"Bearer","refresh_token":"1//0eqq1LhGrDfvGCgYIARAAGA4SNwF-L9IrCZ0lV8i1yjwD0glniNZvv3GsRXGXsKEJrZX0pwygEiIx30lVMiyPOOZgOdGJv3dkVe4","expiry":"2021-08-18T14:21:06.5190624+07:00"}'}, {'id': '45b8051f-b057-4165-83da-f154a1698c4f', 'share_drive_id': '0ABXe8ie-rxVWUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-cKm6IScssDaZs7zZp-W30S98fM__fUfimebfIyGNNXLs-dnbAYzjwtcOIV4uaPA9ozTGJJZYLCjhot9oFCh0iDI9D_lNohTF88OJIzy5qXBwdK0iq28RKUQAiLuEnZLl39H4dfufEWT9I_3uqlyFo","token_type":"Bearer","refresh_token":"1//0ev9uGQ0Xf0DzCgYIARAAGA4SNwF-L9IrPi9mZCRKvvT3Z7mOKaHuN4SZI_CZekty9JL3TROaLBpJgWhaamnhV5kE7gE69TTDn6Y","expiry":"2021-08-18T14:21:28.8232665+07:00"}'}, {'id': '9ff861a4-40f0-47c7-ad0f-8a56890cfda3', 'share_drive_id': '0AINGQVmLbYsCUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_jDKcsUJ1goOgvLbZWJ_3zD_XXQUHvokXwNBcs4whBdQhfeBIQDIHaj1t2n0q6RXRY18zBR0drvOrVk4Bu6q0aRkbWgOTEJo6F-1ouXRn1CYXAgK77J5sVOUS-NLD1lbdyCnUZblbkoiZq2kKSpWd1","token_type":"Bearer","refresh_token":"1//0eI4RYA9IRUjyCgYIARAAGA4SNwF-L9Ir--RhDsbGEzNKmDpuBKLfSoIk44nC_EIIt9pEY1xiLciEx4BwgjCYCPtCFdPthNbyOwo","expiry":"2021-08-18T14:21:48.8429886+07:00"}'}, {'id': '1326a76e-02a9-44d9-8c40-5499b5e3dd1b', 'share_drive_id': '0ABxVds9mPdhjUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_77uqbLV8LZJe-0b6tZ4W-uoBm-NulyFYaTCBXyV5sZe9i2kE14vQnKMKriyXId-qXs8pw0VKwuBhRZsYfg03tabSDC4YqxW8gCpxvfn6BKKbzoSoZmo_M351jau2D7pkdu-4U1419FvwVaPQPk2Qg","token_type":"Bearer","refresh_token":"1//0ejOfei10LH1MCgYIARAAGA4SNgF-L9IrXlh2-T_YYXGQVdy_9bL079c9zrqz7EUlVrY0LV3jBpqbs8f0On873B1pMkzh0J5VXw","expiry":"2021-08-18T14:22:19.1932152+07:00"}'}, {'id': '9eb89921-f7a5-486e-acda-e0c2cf591af2', 'share_drive_id': '0ANUOkQ-g5BglUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_Q6BxZAcAcRCSK6SelvAqjBLp4whIXN-1w4DzUlj0cn6gPnN6ERrlSYjfsyWAOWYfLBYXTuUqI2yzDfiIL1APg3BSYv85C5tof0gg_vZECsN_-0dwOVMzKpvzo30e7Ey2-ipPb3oFx-vlU8KFyFJEn","token_type":"Bearer","refresh_token":"1//0egR0GI2y82OGCgYIARAAGA4SNwF-L9IrJky5ourm_u7PeIO--UufXtKZxbGLArrEdxyQfuj_GxfhRGArgUQSgODHDZihU7pvNUk","expiry":"2021-08-18T14:23:12.1659074+07:00"}'}]

PROCESS_COUNT = 16

RCLONE_TEMPLATE = """
[{mount_name}]
type = drive
scope = drive
token = {token} 
team_drive = {drive_id}
root_folder_id =
"""
RCLONE_CONFIG_ABS_PATH = subprocess.check_output('rclone config file'.split()).decode().split('\n')[1]


def process(abs_file_path):
    os.system('python3 upload_to_gcs.py {} {}'.format(abs_file_path, BUCKET_NAME))


def mount_drive_disk(rclone_mount_name, token, drive_id):
    os.system("echo '{}' >> {}".format(RCLONE_TEMPLATE.format(
        mount_name=rclone_mount_name,
        token=token,
        drive_id=drive_id
    ), RCLONE_CONFIG_ABS_PATH))
    cm = os.system('mkdir {}'.format(rclone_mount_name))
    if cm != 0:
        os.system('fusermount -u {}'.format(rclone_mount_name))
    os.system(
        'rclone mount {}: {} --vfs-read-chunk-size 256M --transfers 16 &'.format(rclone_mount_name,
                                                                                 rclone_mount_name, ))


if __name__ == "__main__":
    processes = []
    for config in RUN_CONFIG:
        share_drive_id = config.get('share_drive_id')
        rclone_token = config.get('rclone_token')
        mount_id = config.get('id')
        mount_drive_disk(mount_id, rclone_token, share_drive_id)
        current_process_path = os.path.join(CURRENT_EXEC_PATH, mount_id)
        while len(os.listdir(current_process_path)) == 0:
            print('List dir not updated yet wait 1 sec')
            time.sleep(1)
            continue
        if os.path.exists(current_process_path):
            print('Current process {}'.format(share_drive_id))
            for folder in os.listdir(current_process_path):
                if folder == 'upload':
                    for file in os.listdir(os.path.join(current_process_path, folder)):
                        if file.endswith('.csv'):
                            p = Process(target=process, args=(os.path.join(current_process_path, folder, file),))
                            processes.append(p)
                            p.start()
                        while len(processes) >= PROCESS_COUNT:
                            processes = [running_process for running_process in processes if running_process.is_alive()]
                            time.sleep(0.01)
                    for p in processes:
                        p.join()

        else:
            print('{} not existed'.format(current_process_path))
