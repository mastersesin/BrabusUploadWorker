# NAY XAI TU 15 - 17
import uuid
from multiprocessing import Process, Queue
import os
import time
import subprocess

CURRENT_EXEC_PATH = os.getcwd()
BUCKET_NAME = 'ty-bucket-farm-18'
RUN_CONFIG = [{'id': 'aaf50543-4635-4974-a51a-cdc7b8bcb21f', 'share_drive_id': '0AGp5sc7gb8ibUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8B-eHE3eAnX5SFKVjnC9ufJPd0M4tYPWTUoRN4OwUYnbBVnkKayUgLcQ7tKaOJNYU7tpimcS6fbY-BR9G1ql3S7FRPWwAyrbHJ21DKYZPViFUO_HspzguhnHAWGotqfogA0k_zZJ9hfwgfg69yt7uI","token_type":"Bearer","refresh_token":"1//0eMgaFcswZiXDCgYIARAAGA4SNwF-L9Ir_VCgq7ovUECAx7HKgqAJlWc0zr4Ihb1g8_aBv3Gzr46-QaZhkps5eyVqJFpFv1fFQls","expiry":"2021-08-18T16:51:59.9567548+07:00"}'}, {'id': '66362c82-22c8-4091-a313-1c4de8e0956b', 'share_drive_id': '0AInCM18jpW-CUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-GYkfZgZQ8KIgSI3sLQhKVvitJBxyqQBpaqfoVSkGUgIS3RP40DrPJ3oHpF0ceaxIueDFxPp9ob7tlJ-dpHstmxYjs_Io5TApSkckRai-OsZiTtIQmgxpn3e53iUt9ekrnrF2RbO_JlnCogbgFM1mm","token_type":"Bearer","refresh_token":"1//0eoxHLWeQkCURCgYIARAAGA4SNwF-L9IrkXMbwrxXfRkLSaELEW5JfU7zfpPqtf1oGIXlVacRWEldWV-gRHmTvGRY0_a-mfgj42U","expiry":"2021-08-18T16:52:30.433712+07:00"}'}, {'id': '3a85e9d9-cdfc-4737-8158-b22bf3061ba9', 'share_drive_id': '0ALhgom6ON9i3Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8U2pf11Ims9UzqLOoApvN8FMtyXofd5c8JFkm2DZ58KYdbjqYXDEoDkfTYncCjLC8tPeh5eG7WyvIGB9-NRRg4wTzk7hVJNEG6lN9Jb_SZXy-Ga70EfECf-DhA5yIxWzLLpqfpMuSfUFy2Ndl6Wqhh","token_type":"Bearer","refresh_token":"1//0eCMl3-OuY2toCgYIARAAGA4SNwF-L9IrHnNyAlB3ey6gdkgBcrNCGEhrde6gwzMdqASjvOLS34gIE46DDFUC8fDdvyy2QISr93w","expiry":"2021-08-18T16:53:05.3447902+07:00"}'}, {'id': '178bfc68-85fa-4cda-9ae7-9aa73cf6db78', 'share_drive_id': '0AIPaqMNSWa8cUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8CP2wV5PQUyD4hRSgUvtlXkaVc_sYPEVIg-K8eGdzHXfY6a8WJQ6u9R_kiYsBqWTtFdNd32p7oXi4sRQwn1xcET6fSzqSi5WxVbwdI3peD5mySi6-OjIcylnBh6Twg4uNKl90Q-GfV8jaFweI3Z5ue","token_type":"Bearer","refresh_token":"1//0ereJ2J3M7uFTCgYIARAAGA4SNwF-L9IrsQTP_0ysbVKirxmmhrIy0WO-1VPUCprI3mctYsMdNBXfqAjg8d87on0jnCS7q7w1-5w","expiry":"2021-08-18T16:53:26.8558282+07:00"}'}, {'id': 'd4292028-4c19-4ae4-bb2e-d8b08cede79a', 'share_drive_id': '0AIM9K65LpC0fUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-swSF4Re4qsCnmhl5cYyk63XRb5HGiCvQSqg8bg60GBHOcVQOncP0-_AUn0V2mCAcOi_nThU8Hb2F4b95wub8kQTzmMD6_d-cw3zKV59WI3WHIGZOVF-9fpI5Em66n-l9g2wbUr7ZqOXEEiJOgYRhD","token_type":"Bearer","refresh_token":"1//0eUZYA9bgpHR2CgYIARAAGA4SNwF-L9IrnrCFWWtSYnncbd_tT4i_N23Ojuj8cSZAWz20SxHM3sRbO8CKcPIXK6ENHHoAH_DUwgE","expiry":"2021-08-18T16:54:14.9733407+07:00"}'}, {'id': '136a1717-cd7a-4cea-b45b-6505272ae025', 'share_drive_id': '0AEwT3OKAHzpLUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9fTZmMrffLSrFgwn23ovQqNPDggKeM-ZK-KaATt00D1-mQaLu1HQsMYyDz__Yg7VsL1_J54dgaf3iUzHCfcYC5VpfIlxJrN_ZERfHWsGyOdlohQR9kOSQqbguaJn6Gu4swxizBtZqgW7GaRMrz8Os2","token_type":"Bearer","refresh_token":"1//0e-PrUu6XMDC-CgYIARAAGA4SNwF-L9IrnLLJswaEl_ZbYD7lysAO5Eft5AU0ECoQingK0dQyZUiPSj0AuegI_sOo-Grn2ZUxT1E","expiry":"2021-08-18T17:00:54.9550096+07:00"}'}, {'id': 'd4c3920d-1320-4321-b86e-18aa4ce0b75c', 'share_drive_id': '0AJUkKSwSBdFBUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_XPzfTn3cXzrxidDI1P9TcCT7Ei1mA8xnfJPcItZ2kl-vkP4lCOZBMa2xgVNI4XnE0bLBiNBcvV8Fac3RA-4AiIaLINVd2uDQCqvdnohiyadd-re0Yu6f5w_hxqyDI8azLNxJCaaDFrHhbUZNnI8u1","token_type":"Bearer","refresh_token":"1//0ej_907aGrhrCCgYIARAAGA4SNwF-L9Irom-enaYq68wF97aOa0fWdMO23QK1xAODSnC-gFOqAteWN16s_IYW2tH3qHGspL6GC9g","expiry":"2021-08-18T17:01:23.9078077+07:00"}'}, {'id': 'd5831e0b-5325-43ae-9e0a-b3eff1686b4d', 'share_drive_id': '0AFSyjmNRTlQ-Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-pGNjodIv2CXaWeqinGwZImJc78KB1BtNFUw50YSHNLaDkd9pwkML20oJpDpZ2NygR2erPvlSWplpH4S8DUZwRmWEHAfnJ4N-Tp9eReYZQ2GDAB-4wEOBcrCSn2-jeAiDbWKCUm0KfS1ReO3H_is-r","token_type":"Bearer","refresh_token":"1//0eeG3uh-4WQLgCgYIARAAGA4SNwF-L9IriW1U0yODc4YSP3b8ISJ-IysvYSJ1_vJsLDIP4GiVto7vuOntFMZc36IeiroeM4d4pZw","expiry":"2021-08-18T17:01:52.8678166+07:00"}'}, {'id': '2a6fe082-aabd-4e8f-9d55-2569c375be00', 'share_drive_id': '0ACutd3nntUPnUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8LbBpmabRjne35MEmeIkB52RjycqnCmZ-DwcLvLxzkZd-TR4eiZ-y5kzW-3lDxBKA2VwO_W44lnTRDbRMfN3u5OH0K-RvfmsDxqHwqA2TkHRt7fKRDWkSCvo8S8ob1vrAn9wzQ4ervxL6-AF7r57ux","token_type":"Bearer","refresh_token":"1//0eVJbFnEpHUtjCgYIARAAGA4SNwF-L9Ir-UZCOp_5SFf-v7kgZ-f9qS-hgWE6moVXRhVKsAfhm1U4c1tztEVPwNagecFZdBuKM9E","expiry":"2021-08-18T17:02:12.7463313+07:00"}'}, {'id': '9ef28e12-3333-409f-814b-10197f7dbf1b', 'share_drive_id': '0ADR0_Y39jMAnUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_tUq-EH3FFeHE2J8cd478_5Tue9_FzQ13oapaWUVWyb91G1sXxC3D95jEPpQlJtcn8WWTeNHrUnzA8krP0P20xl3egjIJ6kujuZUkSn3hSWCapROk_0wQ4xcJCGuFnz-Y8PME3GHupWf2TMzpcNIxM","token_type":"Bearer","refresh_token":"1//0et8r6hWJeEoUCgYIARAAGA4SNwF-L9IrUsId3mHqUyH39N0FoUU-UxAZQxq64enCMR009_XPxEN7v0FPpcB1c-CJFGAmCUq7Uis","expiry":"2021-08-18T17:02:36.2772619+07:00"}'}, {'id': '9c1c1b16-b8cc-40f7-8ab8-d11b7381d257', 'share_drive_id': '0ANK1z6KexU-oUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8ce2rj1bISQFu5Gz6zsIgX9S38SG9rNRnpGjeWYTWdXrH1zm9nJC3wMEZTRehPNfX6otz7jyCulVAeAWPA7tCfwdFWl_2XhKbJ1Rw5VaiklRdG4edLfXF2MDU38wEbG5AVi5sPQWOFvCAfYZUhvK7F","token_type":"Bearer","refresh_token":"1//0e9XILQA5cWEGCgYIARAAGA4SNwF-L9IrcBzJA0y2H0AA5VDIwF8lLKIMD0VI7kFWvfWEuRnkU2xVGCVmXINbY3tb8NrjCI7ce18","expiry":"2021-08-18T17:02:58.6397889+07:00"}'}, {'id': 'd9b6f4af-b4f5-4436-a820-7d3c972f6a20', 'share_drive_id': '0AFi6Beymm0kjUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-DBV5zaostqBCaYAGOgL7avKUEUtaezQ6lS8NQMd7WERU7mKNkBMu2d303cQikb96XSzt1uuhRsZqHOYzhVOf7fEztsWSoNFkTjA17Bo9yYlxt-iRkQM-rupO__SIVr_2rSC8xx8UG_H2IC9J6CzBD","token_type":"Bearer","refresh_token":"1//0eTmCZnqb60iHCgYIARAAGA4SNwF-L9IrT1RK3ngz--IOHqIDEUmlhUbcqCB7dZ4NVONzZz2OImPpv5aX6OG8ZVQpb3mPkJ11o38","expiry":"2021-08-18T17:03:20.7355208+07:00"}'}, {'id': '53f9ed71-8ef0-43ec-8c59-26602139f12e', 'share_drive_id': '0APVzctK0Wp_nUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8-8kGXX170HMDWtxjbFxHeXIQTdNjCESJLNqRKUXGIPbSZycKfwq-fz01yuPsRa3ztqfrK6X2DHbhEI3Jcw0Er8fbtDBPBBiOPi_FMnYYAJ-xRXGklq1lmt1l23yT2fTBTZxVrM7lH56pWiGwknqc0","token_type":"Bearer","refresh_token":"1//0e_tHhfMETnEHCgYIARAAGA4SNwF-L9IrylDv-62UwVkQPDSFq1ognywKv2mozE05BJmsrnYlymOZn8Sil4tMMMGszKst6bAOGso","expiry":"2021-08-18T17:03:45.3603592+07:00"}'}, {'id': '8a182437-368f-4da8-8e50-94b1ba82b76b', 'share_drive_id': '0ADAzFy6EYCwhUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_Nvr0AIxr5eMte90w_mCvf2yL-VHeuzSLuoh4ExK7Uw7ebuZPBMox8BPTz8R0_q27n_eGn_QCAud9s8a0VEpNjFexoy6laVQ5MMjY_QP27KCru56P7stRJbm1vW7PYyc6tzxqwPMrPcMCgLAGHrYpx","token_type":"Bearer","refresh_token":"1//0ea9EJWUSZBcYCgYIARAAGA4SNwF-L9IrcyvG6LUX7og1Gom7MV228vG6kQkEt4gutgbT_sQZLunJPo-C_dEEK-rGSqwSQnGbzUo","expiry":"2021-08-18T17:04:44.298981+07:00"}'}, {'id': '7f7b7d15-39a5-4667-8d55-3e7c4ad5f594', 'share_drive_id': '0APAChqPD-1j5Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8GdviIeFW6u-rL0L_gBtQlc_QGnZwTHZMBNgSHaoBOvBZAsMULD7E_T1Yq6jYdiURbdhvsBf-j5TVWDlln9eWKnO6uxVHvA1Z2fXYuqKzbzIVNzRQVe8W8vdFK6PFeSYGu9jsE5pj5az4xwiiaV6y3","token_type":"Bearer","refresh_token":"1//0ent4MI7nJm0FCgYIARAAGA4SNwF-L9IruLc1Ua0V7G5A-UOv1b3SkQVqVIh4EDa4syEhLIvQMOo4pnVST3rzGInt2zA0fYbUvQc","expiry":"2021-08-18T17:05:08.1617039+07:00"}'}, {'id': '1d133458-d1b9-4802-b23f-8a09d0cca16b', 'share_drive_id': '0ABYhikRCctvvUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM91ZlPhMHxQfBpBI01KufsBuaAZ9bNcLMUKIeYVCI10WQ-yQU8us_9nDqVBMyhS3cbiQGb4kVNbHY63-K7fL31CYI7n3HEHeUFcLkN_wLUkvfIM1LPP_luE2huTgCXGS1nNksYPhgz8HJCzuZUHS0QR","token_type":"Bearer","refresh_token":"1//0eIZ9qoIG0L9RCgYIARAAGA4SNwF-L9Ird8circT_hhWHfTODdiDzNN5ohPud9xGdbn85aHPfsKPGrWcqVSAatXFhPNWBaDhtpmk","expiry":"2021-08-18T17:06:05.7375607+07:00"}'}, {'id': 'c458a7a7-334a-4abd-b795-b6da17f38c35', 'share_drive_id': '0AAkBag7xfbAyUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8yBgn5G_-pfb9KYocHNeMMIdLyXP_8BmhvE32g_juEEDmyKWzOZp26PHm6GPDcVI7vSsjkYThQti7dpQ8yqbExzLFda_GSqVH8RcXX_V8xKae4Q6UnAIIm0SxLiib-34t9Y6OyU7u74t5jEbiuE8eV","token_type":"Bearer","refresh_token":"1//0eHN9ufqo_r01CgYIARAAGA4SNwF-L9IrvNKZ5GXt91ZWhacRb_S_X9ayREyd6dUqu9NdUf0LvIn5AE9gz31dFprRKCiWLenYVls","expiry":"2021-08-18T17:06:24.9936596+07:00"}'}, {'id': '0a32f058-c9e0-4ffe-803c-eaa42fc0981d', 'share_drive_id': '0AMKs7Vu1JNd6Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-Y_4Plps7GrHiYzALzKZ1mpJae_d_hborUpThfavLAVXEnka2EQHemtDBcbdRH2qVZcMTuoSSehUBUQih-cEMHEko7awoI-TXVh37iz1djtiVCcdyQKtj0ZiGadeztiFKzVDJu-aBQWpNp-SAaMZBb","token_type":"Bearer","refresh_token":"1//0ek2PwqvOum_TCgYIARAAGA4SNwF-L9Ircto7jZ4FBeS7c757wdsPhRXkzt52_kg-WBsgHz-uCt17yFd3pcDLn9kIa-PWT2rDYMo","expiry":"2021-08-18T17:07:50.9393004+07:00"}'}, {'id': '165e44c7-5806-4fa0-a19d-2e1b31703227', 'share_drive_id': '0AD1CIEH_rOcXUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_mlZ_kZOFQXe24938ZFhHsms22Lgo6F6uoxU93OHKCH8z0N9da88rmfzdJI_kkjpTYcYKp7mMwLI63gIWdSHAA4u_D7t_zJkSv5M-_B60fLEPcYt4sTX7p9nMGyjY_h-ZJdsL6algzy4k3y7Qm-i6f","token_type":"Bearer","refresh_token":"1//0eMHTJfvyt5hICgYIARAAGA4SNwF-L9IrJkZ7vR7JDrI-PefXJQtoqV_K-7G5NCIF6VBkc_jqVEsCgnPD8PEUs2ypxgISQTOQihU","expiry":"2021-08-18T17:08:13.7843552+07:00"}'}, {'id': '79d0160a-e698-4827-b2f1-5e48d76aaff6', 'share_drive_id': '0AMj7TeuEdJ7JUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_kLCGgqCusEC1-gam4pF-74E4ZWWhv0kC2AB7NMhUVQrsccKChFstGcvayT8zMxUzNOdFZyCTOcU7zG-C4rysz52IyFVDfSvhXOFw9PVm2cRhCw6qoJhThyMC8cUNi_P1FCA2taL-CgYbSIDUh52aT","token_type":"Bearer","refresh_token":"1//0eRbOxd9ZoXYFCgYIARAAGA4SNwF-L9Ir45m0S2FbjJbRY_UT4iOhhmRQXR5YX9pRE4aXP3mFWtJwnzXP93GbSmCsoBRBjTx447w","expiry":"2021-08-18T17:08:37.8697479+07:00"}'}]

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
