"""
Clean entry of the application.
"""

if __name__ == '__main__':
    # Generic freeze support
    import multiprocessing as mp
    mp.freeze_support()

    # Start the app
    import time
    # try:
    from entrypoint import main
    main()
    # except Exception as e:
    #     print(e)
    #     time.sleep(10*10)
