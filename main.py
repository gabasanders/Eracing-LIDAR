
from handler import *
from processing import *
import os


def main():
    processing(pcl)

if __name__ == '__main__':

    #exec(open('mainpcl.py').read())     #Executa o Gerador de PCL

    pointclouds = 'pcls'                #pointclouds = folder que contem as pcls

    #for pcloud in os.listdir(pointclouds):  
    #handler = Handler(os.path.join(pointclouds, pcloud),"outtest.txt")  #os.path.join(pointclouds, pcloud)
    handler = Handler("pcls/pcl_0.csv","outtest.txt")  #os.path.join(pointclouds, pcloud)
    handler.txtToList()
    pcl = handler.pclList
    pcl = np.asarray(pcl)


    import cProfile, pstats

    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.strip_dirs()
    stats.dump_stats('destino.profiler')

    stream = open('destino.txt', 'w')
    stats = pstats.Stats('destino.profiler', stream=stream)
    stats.sort_stats('cumtime')
    stats.print_stats()


    #pip install snakeviz
    #snakeviz destino

    #pip install gprof2dot
    #sudo apt install graphviz
    #gprof2dot -f pstats destino | dot -Tpng -o out.png
    #eog out.png

