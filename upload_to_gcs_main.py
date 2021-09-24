# NAY XAI TU 15 - 17
import uuid
from multiprocessing import Process, Queue
import os
import time
import subprocess

CURRENT_EXEC_PATH = os.getcwd()
BUCKET_NAME = 'ty-bucket-farm-20'
RUN_CONFIG = [{'id': '025f8514-fa0e-4162-8a61-4d0ac5248d1c', 'share_drive_id': '0AMTeToi8M4xSUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_AE2Mcx59esDDa9bdfRVFBg9_36c3uepAqsP9ru_cJI0eLVA8XDY7_xhiUK35mnd2FFRRFA-EIs-76QUx-LKV6ct1UAwIDzC5Pqy6uTr-8JH0fuT0O4CR2vIB0nqv4c-57XaucatgrTOjKsRAgIf_b","token_type":"Bearer","refresh_token":"1//0eOdyQEE0lTMjCgYIARAAGA4SNwF-L9Ir9ors4-GDwKE0HF7hKyqZ4qym3PqJshoySXXbKAMw82OEZf1buXBGr8clIjngkr3dUdQ","expiry":"2021-08-18T17:20:55.122884+07:00"}'}, {'id': '11deeaf3-b4c7-4b00-9c54-daa6eac2c1da', 'share_drive_id': '0AKpNQiG7RV0KUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8aqIIMZ7rKjIlDvuZZJCkCLpoUPl4f9Tk6s00UT9KKzPjvvlLcg_nQ3IQfjJ088wL_tFYyp3hgJP71MSBIwdm0gASa3PcWQ6bi7fGx00Jj84uUVHdDCr4hYD-DQttFw2US08ZTz3vPBUQmGkN7RqYg","token_type":"Bearer","refresh_token":"1//0ejRWbAxohOl1CgYIARAAGA4SNwF-L9IrZ9VzQEDlU0VuJpfGWcQsecY8aKoEW5cOZ6Tv5Eq2qNDd5OKGHD3MUp9D5-tYAr5v1wQ","expiry":"2021-08-18T17:21:13.4333271+07:00"}'}, {'id': '77bb5f7d-9248-4b99-8653-7d2fd6aef9dc', 'share_drive_id': '0AEjK2Q2kk8WmUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_7j2Ck193G3nDHccxAc1j6BtyWd3ncOwyWsiJUIu08NIxv_5Yyl58VHDiICoUeATggG6BJVuH3YtaG7mmVpupZ30pfewdT6dog0N3ERCw8i-qj-HdJKBLgGkJpF2JS5r-cM4BoqdlECeJEdtgK5sDV","token_type":"Bearer","refresh_token":"1//0erabMG6qvP3uCgYIARAAGA4SNwF-L9Ir4AZTAuEDE72oi0C3nZF9xYR0ZnI_wiYcBVIQYYUwUpjuHuJ1h6-_rPP3TUoqye_zyXk","expiry":"2021-08-18T17:21:36.3898538+07:00"}'}, {'id': '51bbf739-08a4-4921-92a0-3ed83dd38d4b', 'share_drive_id': '0AOYILWsJ3xHaUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM99fvNwep80mjSq7E1dsmQ0WLSLOAhvC51LgyMcLlWDl12wV2QemdxQtfA-qqRs0sbq-UjA08bQlQzx_LYVtAL3LXh515h6JzdXfhlCuqFkxYADUxl7Ekp3nD6Om223vxhDKuwWaetI2O6sxlAYbK9D","token_type":"Bearer","refresh_token":"1//0eu-qdyZRbHtLCgYIARAAGA4SNwF-L9IrcaindKOUnc33p0YDLNi_dOrgSbgXkkTPj0sCAGYJD3ZJrPqJFq3apg7UbDWxo4cSeHk","expiry":"2021-08-18T17:22:08.0501874+07:00"}'}, {'id': '0bf56be3-bd5b-4c4f-8fe9-d50c44c83e3a', 'share_drive_id': '0AKQoJMa-J8kSUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM84PAotvR0Q0NF82pZ6H7tvP6RUlwkwNEP2qFsmrsgAvKTc0hURkxOqKQ2UqdqOgI-YsA3gBmi5VOihAJDtT8yxsVyDfLNqtNFZJ0Jn7pCcoWXyaxnTitHuq-795lE-mFoM4ojP_FS_WdgUNsfjXH68","token_type":"Bearer","refresh_token":"1//0esh32Mjf2HHiCgYIARAAGA4SNwF-L9IrHjG9nItmqN0kmi7gFukPOGlMYkyiXfN_caiEAAjCICHOTvpMQ8VTM4LnPPVjkdJgu-M","expiry":"2021-08-18T17:22:26.3790485+07:00"}'}, {'id': '7c17475b-81d4-4b18-b748-7b2f99b0c817', 'share_drive_id': '0AKelepGXpI7MUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8keoBPBzeTP60FV5z7kZps8lTFpV1JSfqwjVxc4Cj-5I-gbIlZbatI2V9ClYkogqdTjabT6PxJ7aD0fok3AP8wgO1AOjx8HqLh5Xwh62qYuT4I5mG5T7iKTtqTpnIotSkc-rO5rbQgj-63GQ-xaaH2","token_type":"Bearer","refresh_token":"1//0eUfKpsEOlXtACgYIARAAGA4SNwF-L9IrCRygqxeR5jL3KZy2BGw7Clv9ngrWlrxEtq3MiUArw80OcInziIAYAgv5Vujv1JL5S8A","expiry":"2021-08-18T17:23:07.7111659+07:00"}'}, {'id': 'b4cb13ab-d238-407e-a643-71846d8c3907', 'share_drive_id': '0APU0jojEyRgbUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8WGJHRCaYyZkc1-pFW1-xs7WIDhd2NZaoIN81CzMjKFiZ-4UcIAwbJEH1OqDnhtLOJX_R7GoCr5RO4IibmSwQV84Z5ps3qv_Apda0685tfYkcT6rdRnQ91xRmfGDUpA0CZDWkVFJfKPHjMU2hMxqtC","token_type":"Bearer","refresh_token":"1//0eeJQGX2PlpH3CgYIARAAGA4SNwF-L9IrRxfDgWIMR4dyl49IIHH2jU0c0Y5_TT5_jK4Qzv9DZCxAX_NLd0jvyVOcvVrTgbvJ6bs","expiry":"2021-08-18T17:23:26.2277692+07:00"}'}, {'id': 'a5d84a3f-a7df-49b0-ba05-3b72a833cdda', 'share_drive_id': '0AFg5hzErB9O-Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8aGEpNCeZfHogjP6vAHYD-OOOZvpNmSSWKH6u-c5j1nuYVCQ6kGVVhBPlVMaKQ4ku_e321Oj1LZAN4WkLMMwN7FWVnUDnLG9xx7bwhmj4ixAY6d0g8jLN4k2K6KHqWxbDbZ5jEI6ipnYhvvwy3idbT","token_type":"Bearer","refresh_token":"1//0e2FatRlAznF-CgYIARAAGA4SNwF-L9Ir4XdPoyZPPWRHi3uLGsBulI655XVVbhEtnPZfpqCbgra204wMUV6kbB3vcQAZE-SI1-E","expiry":"2021-08-18T17:56:56.8318587+07:00"}'}, {'id': '600705fd-aeeb-4bd7-ae22-0343cbc857a3', 'share_drive_id': '0AHELjUkICADiUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-2kd09_0533BTxgDDIriNd4fVQ2vO1uGs35GjF3azNx4KOZiD9AutrIQ_uNL8ZLhgSZsz025w5KPfrkc7SdiF_ELM9PJ1VARb7K4-kNH0OvKG6wAn0k9b5xoC1g8ZTyLT3Q1UH-lYPS9vVYPfb0_Zq","token_type":"Bearer","refresh_token":"1//0edsTopwc4QTACgYIARAAGA4SNwF-L9Ir5vJVKbMBZEXGjCUrPiHXi1_Yj1PJ23NibqgwVp4OSu8NaVrR18U1TfqtKWPnoO1K_so","expiry":"2021-08-18T17:57:15.2236298+07:00"}'}, {'id': 'b998a702-63a8-4089-8f4b-230a45ae516f', 'share_drive_id': '0AIbLldLhF4uIUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8N3MY4gNFF7e5ZArwitg001n9PDGskpsQ_mPz5FTx32U1wpSQs_J3Q9qEQGIFsq0ZsBxCIC1IfTU51B2ELC0036hdxiitrNmSMX0C1uuKKX4TMTWRKrFNZOjAh4MeAEsPazndfkA8IWtZ17CcNE1qy","token_type":"Bearer","refresh_token":"1//0eXrq1QFoSd-WCgYIARAAGA4SNwF-L9IrMsJTIvSkg3cLGXnWKLVj463sryfZ68Vynjisp9HoSqFthZhEoAqXjasgdl8PQaDPugw","expiry":"2021-08-18T17:57:34.3791653+07:00"}'}, {'id': '931779ca-3d85-41d6-a5e9-a44a189c276b', 'share_drive_id': '0AGmhrnElUmvcUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_qNyN6KfOfRh21pzdOWSgaICYXewuugiNUt0P_xYxx-ETXBOjpb99H2OAAsn6TQMEEBaslgyHI3LFl5V_QoG1fVsEe3gHGiPehknO3MXBhmpXGpWGTctZHV3eLQRw-GzJBvqIMlvUwNW4VYhbd6c77","token_type":"Bearer","refresh_token":"1//0em5ScwfPRXdxCgYIARAAGA4SNwF-L9Ir5FfPiURD6eec1hs9rsEfA5xPhNYM10y0yEvQSvziGM6jb2XFDva0yHl6U0PtyCUsi3E","expiry":"2021-08-18T17:57:52.9130138+07:00"}'}, {'id': '2e8d5d7b-d67e-440c-9724-c5f63a337663', 'share_drive_id': '0ABiULzKgfxnPUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_UcyUK79hZrzzxaEx3lQSx8vTlxIXOiiTYlXhcb9b138b-I_naUxP9aeTHTtgzaM1_HkQILNlwIyKHrkjJO0SLtHz5Oa4hJp-KUm7dfteKXNk1cxHFTWw_xGxC2g3_iJ7q9bPmUlNviJ3Kvthp1DrI","token_type":"Bearer","refresh_token":"1//0eK-OaoKoMk8HCgYIARAAGA4SNwF-L9IrYg1jREs2A0svmWtDnrkLYtac_IhY-VV7x8RVeSUvR_jRw22riYYymlyyNE-CRBNzFKs","expiry":"2021-08-18T17:58:12.325797+07:00"}'}, {'id': '25c2fe0e-f255-49dd-8e7d-5a085906f2e0', 'share_drive_id': '0AAvlHna7PmzJUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-1iC4f01NIQoZDHJeKiRL3fU486au-XTeD2v9TTvMOPb4b75JaZyO2s4GNdZdQy2OfQmxOu2Q1vYBDXlBGBSS0BZIu1x8BwqQcIM7DUIfdh40gmymQAjeHOUyAzwDtMCujWdGJ6ljYQGLWNxD8RNeG","token_type":"Bearer","refresh_token":"1//0eqB-OEuq2KkxCgYIARAAGA4SNwF-L9IroJov-avKSLou-A4hOfrwIbFt05HaOFBJxorIr7pGRYA209EoWYR9LKLfleg1exctMUo","expiry":"2021-08-18T17:58:51.1117722+07:00"}'}, {'id': '8903d772-d591-47c2-8f15-4a1aad6374b6', 'share_drive_id': '0AL4L7lfDbFCMUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM87tYyrsbxelZ94XD8nhm0xiDqQZN8xftJJ3f0OsffzODiMdR9ZJsuts6UgowFhh1mldLwQ3RF0TMVeIuhZIMGaef3D-k6oxwoZWWPmmyLJlrhxwdxh_kLaYpGVgaG3wxWODmpYuXdc3fAf9iLObI-h","token_type":"Bearer","refresh_token":"1//0ejyaJWyzJS5XCgYIARAAGA4SNwF-L9IrRt5sh3glYPkEwgRu6e_iUJXEXh2Gp1NJtgwvfR_AP0Ids0A0e5SkLvo8OtxRgd36GwM","expiry":"2021-08-18T17:59:10.1335999+07:00"}'}, {'id': 'fcce7a3d-460e-45b6-91cd-4beef80a64a7', 'share_drive_id': '0ANNL2hQyVjRRUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM85TGhx5MdhmHTaiySWB5rwgohNJeuLkpdq3YTBE97h_ga6AijJzbBi66AntYC8UeNCOQarWbLOJJLcZMffbSzdl10-EbUazC3t_vWtu6boIK1LZmXyqjm4exnnJF6bCSRYs7uzSEityJyz3nBbdsrY","token_type":"Bearer","refresh_token":"1//0eCRrGrMf-8nPCgYIARAAGA4SNwF-L9Irvj6DEnJUI0zQhhF4LMNEb0AeX_FAt-xnDJjHiM1waW3YdluIBc11gHpj6emEmQ1ibn8","expiry":"2021-08-18T17:59:28.9706329+07:00"}'}, {'id': '70d79fe0-846a-4ffe-9e16-317720d5b7cd', 'share_drive_id': '0AB3tTHFtG9vnUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM87XxrJrz7_ojW34LR6aW8aXWhklnwALz-Y1cZEboUKvWOrPtxKJW6uh5IPHW5EXSd_JVxcJEqLV744Qi-VFsnmURHoXor8m_0lKNu1XkIj-UE11-QkxD_VNnG4NxXRznna-QXweQbfCu_1TMu5QsfQ","token_type":"Bearer","refresh_token":"1//0erxTF2vWEm5uCgYIARAAGA4SNwF-L9IrGzPFGRq1PwtzpIa5Pdrgb390oPMpufgCKmqbneHBPJR5OAzAa3a1DxNR9NL6ndUw28g","expiry":"2021-08-18T17:59:54.3118044+07:00"}'}, {'id': 'e08c299b-210a-4083-8b58-bca430588f8c', 'share_drive_id': '0APAQcwkUnZLXUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_vJqgIhh0USGARXKL-82nuMTxn8Y50iq-KxrzbsTdBGnGoGOhwyT97YXXUWXGFt6wyiXOVc0hlk20VwRngrbKCwmjuEZsledIUfLPU_eI96PnVcZ-shjxcj-CYCGM4zAp-KCza_3-6c5ecfWIWKw1l","token_type":"Bearer","refresh_token":"1//0es-blbjS1cUjCgYIARAAGA4SNwF-L9IrF8z5T3YmbhnB91QQljCRmU7jEgaX4xYMZ8Tp2lwYb44IW7dsYFucDXF3S7t8jo8ST_0","expiry":"2021-08-18T18:00:13.3013895+07:00"}'}, {'id': 'e70027f8-3c4b-431b-be06-a6e4f1e38025', 'share_drive_id': '0AFgTgFqYZQ1nUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9bo7CfFWEKwor2amK-SJLb7S5n5TpNbAC_w56x-xpBaxr19f9r8fyka3Ae0_aKlCgakh0S7-VhM2Jufz5NtHQc4s0ok61kbVACLblGdc1TzzMO01DSRhAHDaZlLenWQa-0HfoVmXkxdHKMdMU6je9O","token_type":"Bearer","refresh_token":"1//0eF68Vfsh-UkfCgYIARAAGA4SNwF-L9Iru_M2torazBh13a49Gbcta4vlV3wE0pvJHtGURt31aM7_dZEMjWF9MYjFy1WD6IUN9HI","expiry":"2021-08-18T18:00:32.1397908+07:00"}'}, {'id': 'ad9fc518-e01c-4785-a6ca-0f25675ee554', 'share_drive_id': '0AFrRTvoccauUUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_22OprNPEAbsxe2cGBQtzWqNwdrvveoNGTRQQMsT3TlxPJ-MKZMRMwBKjSiXQxfx1sTcr4sbPW5GtOtxT0BbUUoETXyG3-_bqWvciRaYFIWPeHHnhP8AY_281G3SMIVJiTTmi6M55r78Gz-r-dTMAO","token_type":"Bearer","refresh_token":"1//0e0P5bJGtrvnwCgYIARAAGA4SNwF-L9IrCuYyZaKKeMTnXNLvSO-rrFRVAoamThEKZ796rZGpvUjU8qifmL8POAg4SJHQgSBTXnM","expiry":"2021-08-18T18:00:51.8799223+07:00"}'}, {'id': '7219a2ec-df47-4cca-861a-499ddba2c936', 'share_drive_id': '0AGbBjoDOim8qUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_XfcpNNkpkemjwN4BxsUYx0QN5BLOq3OYZD6hzmngVvWEkU113_gMFyAyERbtI84z4PL-Tky0qFbkgOyoGa8UffIbmg3toqUkcuSKHCKSzbdAB6ILYCy_ZiVe15VKabJTsYwLBf6RGuU2oWHb_cRv8","token_type":"Bearer","refresh_token":"1//0eUvHcqM39IQMCgYIARAAGA4SNwF-L9Ir9zMxSp7mMPnfRNr_DP01nE9j9hxdGIR33Cw9RO5lSNR3674On2CiEHyqOBEqiZ5BmSk","expiry":"2021-08-18T18:01:19.271579+07:00"}'}]

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
