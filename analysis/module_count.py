def get_module_count(health_path,ibd_path):
    health_module_set=set()
    ibd_module_set=set()
    # read health file
    health_file=open(health_path,'r')
    for line in health_file:
        line=line.strip()
        l1=line.split('\t')
        health_module_set.add(l1[1])
    health_file.close()

    # read IBD file.
    ibd_file=open(ibd_path,'r')
    for line in ibd_file:
        line=line.strip()
        l1=line.split('\t')
        ibd_module_set.add(l1[1])

    print("health module count:")
    print(len(health_module_set))
    print("ibd module count:")
    print(len(ibd_module_set))


def get_common_module_count(health_path, ibd_path):
    health_module_set = set()
    ibd_module_set = set()
    # read health file
    health_file = open(health_path, 'r')
    for line in health_file:
        line = line.strip()
        l1 = line.split('\t')
        health_module_set.add(l1[1])
    health_file.close()

    # read IBD file.
    ibd_file = open(ibd_path, 'r')
    for line in ibd_file:
        line = line.strip()
        l1 = line.split('\t')
        ibd_module_set.add(l1[1])

    print("common health module count:")
    print(len(health_module_set))
    print("common ibd module count:")
    print(len(ibd_module_set))
def main():
    health_path = "/home/zc/IDBdata/experiment876-result/module_ibd_ex7_test.txt"
    ibd_path = "/home/zc/IDBdata/experiment876-result/module_ibd_ex7_train.txt"
    get_module_count(health_path,ibd_path)

    common_health_path = "/home/zc/IDBdata/experiment876-result/module_ibd_ex7_test_valicommon.csv"
    common_ibd_path = "/home/zc/IDBdata/experiment876-result/module_ibd_ex7_train_valicommon.csv"
    get_common_module_count(common_health_path,common_ibd_path)
main()