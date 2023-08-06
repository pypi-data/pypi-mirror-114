import sys, os, atexit, datetime, argparse, json, logging, shutil
from multiprocessing import Process, Queue, Lock

from simple_image_compressor.src.settings import Settings
from simple_image_compressor.src.job import Job
from simple_image_compressor.src.compressor import Compressor

def arg_parser(conf) -> argparse:
    """Parse the arguments"""
    parser = argparse.ArgumentParser("Simple Image Compressor")
    parser.add_argument("path", nargs="+", help="path to the directory to compress")
    parser.add_argument("-v", type=int, choices=[0,1,2,3], default=1, help="verbosity level: 0=log file, 1=print dirs, 2=print files, 3=print json")
    parser.add_argument("-s", action="store_true", help="soft compression: doesn't resize, just compresses up to 80%% quality")
    parser.add_argument("-t", action="store_true", help=f"temp output: doesn't replace source images, instead saves compressed images to {conf.settings['temp_dir']}")
    parser.add_argument("-n", action="store_false", help="no exceptions: process files even if they're in the exceptions list")
    return parser

def process_start(queue, results, lock, job):
    """Process items from the queue"""
    try:
        while not queue.empty():
            queue_compressor = queue.get()
            queue_result = queue_compressor.run(lock)
            results["q"].put(queue_result) # using a list as mapping type to pass by ref
    except KeyboardInterrupt:
        job.status["forcedStop"] = True
    except Exception as e:
        print("An exception of type {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
    return

def process_terminate(processes):
    """Force the termination of the processes"""
    for process in processes:
        if process.is_alive():
            process.terminate()

def main():
    """Set up everything and starts the process"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    logger.propagate = False

    settings_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../res/settings.json')
    conf = Settings(settings_path)
    job = Job()
    job.status["timeStart"] = str(datetime.datetime.now().replace(microsecond=0))

    parser = arg_parser(conf)
    try:
        parsed_args = parser.parse_args()
        if parsed_args.v == 0:
            file_handler = logging.FileHandler(os.getcwd() + conf.settings["log"])
            file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S"))
            logger.addHandler(file_handler)
        else:
            logger.addHandler(logging.StreamHandler(sys.stdout))
        conf.edit("source_dir", parsed_args.path)
        conf.edit("verbosity", parsed_args.v)
        conf.edit("soft", parsed_args.s)
        conf.edit("temp", parsed_args.t)
        conf.edit("exceptions", parsed_args.n)
    except SystemExit as se:
        logger.critical(f"Couldn't process the arguments: {se}")
        exit()
    except Exception as e:
        logger.critical(f"Couldn't process the arguments: {e}")
        exit()

    if conf.settings["verbosity"] < 3:
        logger.info(f"\r\nStarted processing image files in {', '.join(conf.settings['source_dir'])}")
        logger.info(f"Job config exceptions: {conf.settings['exceptions']}")
        logger.info(f"Job config soft: {conf.settings['soft']}")
        logger.info(f"Job config temp: {conf.settings['temp']} " + (f"({conf.settings['temp_dir']})" if conf.settings['temp'] is True else ""))
    else:
        logger.info("{[")
    
    try:
        job.result["dirs"] = Compressor.scan_dirs(
            parsed_args.path,
            (conf.settings["params"]["exceptions"] if conf.settings['exceptions'] is True else "")
        )
        if len(job.result["dirs"]["included"]) == 0:
            raise Exception("directories can't be scanned or were excluded by exception list")
    except Exception as e:
        logger.error(f"Error scanning sources: {e}")
        job.result["dirs"] = {"included": [], "excluded": []}
    else:
        if conf.settings["temp"] is True:
            try:
                os.makedirs(conf.settings["temp_dir"], exist_ok=True)
            except Exception as e:
                logger.critical(e)

    count_dir = len(job.result["dirs"]["included"])
    if count_dir > 0:
        count_cpu = os.cpu_count()
        count_processes = count_cpu if count_cpu < count_dir else count_dir
        processes = []
        
        atexit.register(process_terminate, processes)

        q_tasks = Queue()
        q_results = Queue()
        l = Lock()

        for i in range(count_processes):
            processes.append( Process(None, process_start, args=( q_tasks, {"q":q_results}, l, job ), daemon=True) )

        for dir_path in job.result["dirs"]["included"]:
            q_tasks.put(Compressor(dir_path, conf, job, logger))
        
        for process in processes:
            process.start()

        try:
            for process in processes:
                process.join()
        except KeyboardInterrupt:
            logger.info("Process interrupted by the user.")
            process_terminate(processes)
        except Exception as e:
            logger.critical(f"Main exception: {e}")

        job.status['timeEnd'] = str(datetime.datetime.now().replace(microsecond=0))
        job_time = datetime.datetime.strptime(job.status['timeEnd'], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(job.status['timeStart'], "%Y-%m-%d %H:%M:%S")

        while not q_results.empty():
            r = json.loads(q_results.get())
            job.status["totalFiles"] += r["status"]["totalFiles"]
            job.status["processedFiles"] += r["status"]["processedFiles"]
            job.status["skippedFiles"] += r["status"]["skippedFiles"]
            job.status["totalSize"] += r["status"]["totalSize"]
            job.status["totalSaved"] += r["status"]["totalSaved"]
        
        if conf.settings["verbosity"] < 3:
            logger.info(f"Files: {job.status['totalFiles']} ({job.status['processedFiles']} processed, {job.status['skippedFiles']} skipped)")
            logger.info(f"Source size: {Compressor.convert_unit(job.status['totalSize'])}")
            job_new_size = job.status["totalSize"] - job.status["totalSaved"]
            logger.info(f"Compressed size: {Compressor.convert_unit(job_new_size)} ({Compressor.convert_unit(job.status['totalSaved'])} saved)")
            logger.info(f"Time: {int(job_time.total_seconds())}s")

        if conf.settings["temp"] is True and os.path.exists(conf.settings["temp_dir"]):
            shutil.rmtree(conf.settings["temp_dir"], ignore_errors=True)

    if conf.settings["verbosity"] < 3:
        logger.info("Process finished.\r\n")
    else:
        logger.info("]}")
