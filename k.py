import pyaimp


def appliactionInit():
    try:
        client = pyaimp.Client()

        state = client.get_playback_state()

        if state == pyaimp.PlayBackState.Stopped:
            print('AIMP actually doesn\'t play anything')
        elif state == pyaimp.PlayBackState.Paused:
            print('AIMP is taking a break')
        elif state == pyaimp.PlayBackState.Playing:
            print('Rock \'n Roll baby')
    except RuntimeError as re: # AIMP instance not found
        print(re)
        subprocess.call(f"start http://localhost:{port}/welcome",
            creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
if __name__ == '__main__':
    appliactionInit()
