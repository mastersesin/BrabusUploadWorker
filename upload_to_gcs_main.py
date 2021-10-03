# NAY XAI TU 15 - 17
import uuid
from multiprocessing import Process, Queue
import os
import time
import subprocess

CURRENT_EXEC_PATH = os.getcwd()
BUCKET_NAME = 'bucket-new-1'
RUN_CONFIG = [{'id': '3cd23a83-8e0d-4e99-8a5d-596253d3fe6c', 'share_drive_id': '0ACBTGm33FgLZUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_M05-iqll3Idh8trXG_SGtYE1e7U3zc2OIwRm8P5-IhGF2lLN2wxB4KuwaChfbTmtdNGZLR0GF63B9C2ts2iD5oDyF61DtnUHgAkGLt9Vt2pQq4BLdCe1uVGdomb5JV771s_Vy_3KgTdGTIbmjFweG","token_type":"Bearer","refresh_token":"1//0e7keAsyNiE21CgYIARAAGA4SNwF-L9IrPEh9wVD8iVE8u9v14Wky1BjLOsjX7RE7KefT8C69tAanZBKF1rJYDDLiHmDibQVWGu8","expiry":"2021-08-18T14:04:52.2720643+07:00"}'}, {'id': '5e77daf1-6ae9-46d1-90c9-8ad1a0e4c1fa', 'share_drive_id': '0APfTq-k5SMwLUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM98tadXGlXQA9jQ3JCzVPXcSJk0qlDrurc7iswxHMUKZpNgQ3UJ1ajSa-jXfcAt5JmtyM6tZJ6rUMURDNykT-d3U7vVISuzHQu7GdGGkXBwYib1c4tu3nk9ySBRO22Jbe2VkduNSUs7g9lZ244skDWW","token_type":"Bearer","refresh_token":"1//0emImTAfriNIECgYIARAAGA4SNwF-L9IrizCoH-5rZtiPyjnK7J062Q0Roi8z4TAIJjUCQ3CegFkVa9YjeXBAjlzHPxvsAESAq34","expiry":"2021-08-18T14:05:50.3927271+07:00"}'}, {'id': '61c7b082-0475-41e2-a523-a2a29903c295', 'share_drive_id': '0APlvlA01k_QHUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM85VErNuOBtDpOWZx4qG4LQx0MZA9Fer2mUjK_PxzZLaGBZRyGnc6W7XwnrYgELneS19LJ3kWlu4he9mMGpzIBsRpmkvFL3Sgrq9Mrq_7zaJoUj9UuNDqN_QvqULfaxMxKqjXNZuUlgr2qaAgQmC8LN","token_type":"Bearer","refresh_token":"1//0eDb11FHL8DCtCgYIARAAGA4SNwF-L9IrHYf_xsUCYpPsAi99P7i4hQpYnqqGjltxILe_o-gD0Uu8PWI9i9TXIADBLNll8rKgMnc","expiry":"2021-08-18T14:06:17.9415136+07:00"}'}, {'id': '08b0c27c-5811-4dc3-b90f-f489b4392b12', 'share_drive_id': '0AHnOWVlWRrIYUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9tu709t5x5rpLEBBpJQPWj49fZsNuzP906ECKbnFHbmSu0kYWuKlJziPwBWHED3HXXv0Xk_pfYJPZJ7vOq5fHl8rPvS-TxnqeozQNo2rQ_6nJ4sMsdVo7bmigrcIYc-mrAD51mw8INaVLSjPY3Nhy9","token_type":"Bearer","refresh_token":"1//0eubJO7eO10zOCgYIARAAGA4SNwF-L9IrrleqXGmP7fC_amUVCMZoAdus0rDF3nXYsoirKM2CPM5xyDPbv5ekEUblorkrRyeXAMk","expiry":"2021-08-18T14:06:41.8943525+07:00"}'}, {'id': '2580d0c2-8f4f-4cb9-8d98-db638a9a51eb', 'share_drive_id': '0AGxrlAzUG6d7Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_TmG3jDtv_HhuRv-wMnzylP0Sc7pzo_KTzidz9CXYTHuXVoFawHra7FaHS1yp9mudynKQJNWSo5NNrmKQfRVA5DpM82oh5LW3uMQxMT1-vCek7xCqpIWMIkuCotQjhOrkjIt1FynyD6-ue3x-5twwn","token_type":"Bearer","refresh_token":"1//0e1c5wJ6H5DhkCgYIARAAGA4SNwF-L9IrQcFbUBmjYrkyIacnwx44WMPwvw9NV89S0R-_rbpe6BJxOhtq_VuTTlFETHfcXb5J9Yc","expiry":"2021-08-18T14:07:06.1655253+07:00"}'}, {'id': 'e21c84da-8377-494d-a388-001b58a1b8ea', 'share_drive_id': '0ABBwxzCTVCrxUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_iPoc9zST3zFrAAqA6hothAeusb20qwSLhtkIkgKqNCdhI8UWN0YDB3C1AVqCbMbcieUISyJBwshuAPJu8kOjX28VWgjy-3VJwgV_ZXtaPjbiZNEGdGsBrgVVfrdzwgULZ45silabWfmFRoohQK5io","token_type":"Bearer","refresh_token":"1//0elaztZ4vkS26CgYIARAAGA4SNwF-L9Irk5bkDGSN8qdGRFznpIeEQXXTco-UWnbeMhcIR2CC9s5vIBUHSgOmfeRCb4rndHLenkY","expiry":"2021-08-18T14:08:11.5419379+07:00"}'}, {'id': 'e6ae4190-cb5a-483a-9533-b431f40854bc', 'share_drive_id': '0AO0ODkAuAit_Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_-FtS1z8YSSoTfbJ9Trra0v2aBgAmbo_N1t7W6GHc7Awf2HzPHx68m5yi1b-1lc0xxfkixs3pQT2tkfxR1KIjCnKFVKJ1eX7Jh72eCJAUYtKsFqOCq53DeQqocM9kH_dsQsuXy4YkxayBUM78pkodB","token_type":"Bearer","refresh_token":"1//0e7v9Gm0aTh5wCgYIARAAGA4SNwF-L9Ir99XrCOzN2j9lISRSYEsDRMDSiB5VJ0yZPrm3ZkcvpFAfh2cAY7l8iJU4ECWYafy5Ph0","expiry":"2021-08-18T14:08:36.3854191+07:00"}'}, {'id': '71d91943-d36e-4457-986f-441e4f214882', 'share_drive_id': '0AKbh8UZjPZYgUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8EAkm7iTjQT6-N-_JjRKC3Z69GCZlvohM1ooQsuzRsZD_gC2_fXRPDrW4oKVM5kqu68-w0Jqmm9SUldhrIikbsQviudZDqkGY7QtbcLGHNFN-Eg39CIJHmNkPhVCSjtJnh3Yj3Fg0keSTjzXlDcpWS","token_type":"Bearer","refresh_token":"1//0eYwTvZcihS_VCgYIARAAGA4SNwF-L9IrQMEV0LtUp3Cz7cXXFOi9kdMrBj1qJiXJFLAwWC4MPQr7dWGBwA_Y9IWr2Fi9BbLgBY8","expiry":"2021-08-18T14:09:11.6548198+07:00"}'}, {'id': '71754122-f04e-429a-be85-8146ce5f574c', 'share_drive_id': '0ADNLKVwyjAp_Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_S-9YmtSv6jTlIowRpgRs4x6D1jZnt1_Yb0aootqrnGUFxR848cnE9vV3c1Lt7D-SKK8_AfExVrJpJjxLH8R8qXw76EQJ4A2wSS7nXnxcjICB2Jmg3GA0XlXqMJYd3Cg9lC6i7GO2XrB5HihbnfvCB","token_type":"Bearer","refresh_token":"1//0ekXIRkEIaNCwCgYIARAAGA4SNwF-L9IrLPXDeoZv03gnFP2_o-olXIX6_UbF2KWDVJAVCeOJObD4_STkjeBJSEjZ81XehaY5ZgQ","expiry":"2021-08-18T14:09:43.6783757+07:00"}'}, {'id': '4580de07-cc32-4c1a-8260-11175ef39150', 'share_drive_id': '0ABWLOfMXRW9xUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9Gvs1PjDSLLb09DzvDOlt-V9SZ5exf-NV6zXpmKWbWeLWKhvt8fNMs7aUZOLdt7IpOMQW2jZcy3sIS-OkfQp9Ox89M7ImdksvGR9W2UnJFWxJZkWTgEzSHGp-mr3o8bkWk0nvF--zEAVoImPDgM513","token_type":"Bearer","refresh_token":"1//0e44degUO2MovCgYIARAAGA4SNwF-L9IrydvtmWKP8u6OOMp7kHmbJ52hXMMWKOtP_W34FskXYz3U-V7dHPy-iVZwBV3BKnk99hs","expiry":"2021-08-18T14:10:06.1790713+07:00"}'}, {'id': 'd7b9f7c6-e770-4cb9-a528-d5f1d772a79d', 'share_drive_id': '0AJzZ5tzrCSBdUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_LLmdQOdey5Gb2s2G1Ln5MCWOYgX0pn7F5oCnkW34sYQtItBExNV3tW4HtdvLHw565b2EB9cH9bJrqMt8VG2fcCVbl6V1Gr9fG6SAOgf7_EziR6Rj_HistGAvY6OSKtmhnKwm57at2PaCTepDMa4tT","token_type":"Bearer","refresh_token":"1//0eAehLomLv3Z4CgYIARAAGA4SNwF-L9IrwDvUJ2-IL9g3f5HOPOjaRxbnIz1m-JlVeGepIticddSDD3MtgIcPwzfc1L8sAcbA884","expiry":"2021-08-18T14:17:34.8704993+07:00"}'}, {'id': '18734829-ba73-432b-b7c1-f4ea7a425072', 'share_drive_id': '0AL4azwN-aGxtUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_jK1mAwcTPH4eDBeeYTWjMjGIlfNiAFYnJ5mIdK8nvdT7m6NE-bDTcODV3wvEil-leU3rT68TMnZZous6WwDACahDI7SKDhHq-qsRCMDXP9-Iq2TD8zpuCQ-ZpllpVd7JQPFcD64TWf7Q8EfJSsZz_","token_type":"Bearer","refresh_token":"1//0eHEvoSI0GuwsCgYIARAAGA4SNwF-L9IrzVTstH4qb5BN1R7JplJYNJ_KrzhBOh7cnRBhmEQs_PrtKfE9TjBcP4_pdk0UpMCFvMs","expiry":"2021-08-18T14:18:02.120876+07:00"}'}, {'id': 'c6daa41b-ccfb-4f02-a6d6-634e1ea9816a', 'share_drive_id': '0AKER4oiKHbx2Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM86lEsjC7NCsMt6jHEKOGmauIi5FVXBxuLnsRIk8Mw_0_k2-5wVFr0LpJChf1fGEaXZ4iW2-ABQHCeuKgdtxL2rn3MNb19q2jJvegzPi2KX8XuLrmHVUKW9c6CtliDeJxksKtzJXori3sE1M3Vj1sKk","token_type":"Bearer","refresh_token":"1//0eWi1ayt-7K2-CgYIARAAGA4SNwF-L9IrvTOztOdPmpgu34QvvvgPSFCqJRpzX17k6h8PQvUWE_nycDt-l7PCnhAGU_Ua_wf4B3A","expiry":"2021-08-18T14:18:32.0753091+07:00"}'}, {'id': '4bd9d713-dd36-4fb1-8059-3693c4a1da4e', 'share_drive_id': '0AJnsxWqtv-0qUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-MY2dUu8qynumI1kR3Kc30uOLbBmqu6m2OFiK3M5uvWd-YvQNfWlCIvYwCpiyws9zgA-xO1mqLDVkA6Gn0gLCaL-x6h1pi7uz_i_Zm8LD7rldFm3_F0L_BDntK23JRMXTAOxdcLMlMK2LSlZ6lYdTZ","token_type":"Bearer","refresh_token":"1//0eiuldKYpMjHcCgYIARAAGA4SNwF-L9IrtsYK3Gdt0yxwQrjJCT3OhOeYweZt2-NdEOs-ecu_iducM36RExRPdtVU6jH8zyT9PHQ","expiry":"2021-08-18T14:18:53.33193+07:00"}'}, {'id': 'e667d132-8f6f-4a53-b3fc-4ecc0b69d30c', 'share_drive_id': '0AGJ9cRkCIBMxUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM--TN-Jjk64mtn6yJ4BnbRxuOR4P9dlYdV7zs1UU5o1caK68on6yh6iUYumq9XEDZj_BOjzcFUrt5NfNMJvzzCnmq84esx0ah1s9w97VU0FJc9LC2VI6kzq6RvU26JRA6hIYXMczBa7PRsD2WmZIhAy","token_type":"Bearer","refresh_token":"1//0esWLHZcAYmEuCgYIARAAGA4SNwF-L9IrS-Dr5JETd6Ncec8ixD0TLdRu4ebwfveg2mAhfIHu0gzCErjzPeDsXPJPFG2nj5axCS8","expiry":"2021-08-18T14:19:19.5777359+07:00"}'}, {'id': '48eeb8e5-1fbe-4136-bad2-29fe2ead5e81', 'share_drive_id': '0AN8-i5pPv5PwUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8C1Y8ZJzuEYePIeK1WnwnO8Xt0Lg25_apsnSLNjOCQk_VFX1i_hs5u19OCFlYDKvX5Bapvg2tlnvMWQsgkKdlmR-a6Zuv70-t6X-NkJPnl2bov5RWIXwLO54RIY1wJcMIqDPuZzOwqkY3osXia9YCF","token_type":"Bearer","refresh_token":"1//0eqq1LhGrDfvGCgYIARAAGA4SNwF-L9IrCZ0lV8i1yjwD0glniNZvv3GsRXGXsKEJrZX0pwygEiIx30lVMiyPOOZgOdGJv3dkVe4","expiry":"2021-08-18T14:21:06.5190624+07:00"}'}, {'id': 'cdbeac99-780b-498f-970d-52fe30ca1db4', 'share_drive_id': '0ALv6gFraOWULUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-cKm6IScssDaZs7zZp-W30S98fM__fUfimebfIyGNNXLs-dnbAYzjwtcOIV4uaPA9ozTGJJZYLCjhot9oFCh0iDI9D_lNohTF88OJIzy5qXBwdK0iq28RKUQAiLuEnZLl39H4dfufEWT9I_3uqlyFo","token_type":"Bearer","refresh_token":"1//0ev9uGQ0Xf0DzCgYIARAAGA4SNwF-L9IrPi9mZCRKvvT3Z7mOKaHuN4SZI_CZekty9JL3TROaLBpJgWhaamnhV5kE7gE69TTDn6Y","expiry":"2021-08-18T14:21:28.8232665+07:00"}'}, {'id': '7f2fe1fa-f343-4fe6-b5d0-7879523bb244', 'share_drive_id': '0AFbLDgFFNYY6Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_jDKcsUJ1goOgvLbZWJ_3zD_XXQUHvokXwNBcs4whBdQhfeBIQDIHaj1t2n0q6RXRY18zBR0drvOrVk4Bu6q0aRkbWgOTEJo6F-1ouXRn1CYXAgK77J5sVOUS-NLD1lbdyCnUZblbkoiZq2kKSpWd1","token_type":"Bearer","refresh_token":"1//0eI4RYA9IRUjyCgYIARAAGA4SNwF-L9Ir--RhDsbGEzNKmDpuBKLfSoIk44nC_EIIt9pEY1xiLciEx4BwgjCYCPtCFdPthNbyOwo","expiry":"2021-08-18T14:21:48.8429886+07:00"}'}, {'id': '1cf703e4-de0d-443e-b2c7-3acf695ef314', 'share_drive_id': '0APVKf7L7g33ZUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_77uqbLV8LZJe-0b6tZ4W-uoBm-NulyFYaTCBXyV5sZe9i2kE14vQnKMKriyXId-qXs8pw0VKwuBhRZsYfg03tabSDC4YqxW8gCpxvfn6BKKbzoSoZmo_M351jau2D7pkdu-4U1419FvwVaPQPk2Qg","token_type":"Bearer","refresh_token":"1//0ejOfei10LH1MCgYIARAAGA4SNgF-L9IrXlh2-T_YYXGQVdy_9bL079c9zrqz7EUlVrY0LV3jBpqbs8f0On873B1pMkzh0J5VXw","expiry":"2021-08-18T14:22:19.1932152+07:00"}'}, {'id': '3ef9352e-68ae-483b-94bc-6cee1b5054bc', 'share_drive_id': '0ABN6NJcC0rkHUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_Q6BxZAcAcRCSK6SelvAqjBLp4whIXN-1w4DzUlj0cn6gPnN6ERrlSYjfsyWAOWYfLBYXTuUqI2yzDfiIL1APg3BSYv85C5tof0gg_vZECsN_-0dwOVMzKpvzo30e7Ey2-ipPb3oFx-vlU8KFyFJEn","token_type":"Bearer","refresh_token":"1//0egR0GI2y82OGCgYIARAAGA4SNwF-L9IrJky5ourm_u7PeIO--UufXtKZxbGLArrEdxyQfuj_GxfhRGArgUQSgODHDZihU7pvNUk","expiry":"2021-08-18T14:23:12.1659074+07:00"}'}]

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
