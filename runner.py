import subprocess, os, csv
import json

output_dir = './output'
if not os.path.exists('./output'):
    os.makedirs(output_dir)

times = 0
while True:
    try:
        times = int(input("How many times do you want to do the clustering: "))
    except ValueError:
        print("Not an integer")
    else:
        break

def run(cmd, f):
    my_csv_writer = csv.writer(f)
    for i in range(times):
        result = subprocess.check_output(cmd, shell=True)
        result = result.decode('utf-8')
        result = json.loads(result)
        my_csv_writer.writerow(result)
        f.flush()
    hamming_distances, mis_errors, iterations = [], [], []
    f.flush()
    f.seek(0, 0)
    for row in csv.reader(f):
        hamming_distances.append(float(row[0]))
        mis_errors.append(float(row[1]))
        iterations.append(float(row[2]))
    l = len(hamming_distances)
    print("\n" + f.name)
    print("min hamming distance: {}".format(min(hamming_distances)))
    print("min misclassification error: {}".format(min(mis_errors)))
    print("min iterations: {}".format(min(iterations)))
    print("avg hamming distance: {}".format(sum(hamming_distances) / float(l)))
    print("avg misclassification error: {}".format(sum(mis_errors) / float(l)))
    print("avg iterations: {}".format(sum(iterations) / float(l)))
    f.close()

# datasets
datasets_name = ['wine', 'breast-cancer', 'bank-note', 'iris-type']

for name in datasets_name:
    f = open('./output/k-means++-{}-unnomalized.csv'.format(name), 'w+')
    cmd = 'python3 ./main.py k-means++ 0 class --attributes datasets/{}-attributes.txt --train datasets/{}-data.csv --normalize n'.format(name, name)
    run(cmd, f)

    f = open('./output/k-means++-{}-nomalized.csv'.format(name), 'w+')
    cmd = 'python3 ./main.py k-means++ 0 class --attributes datasets/{}-attributes.txt --train datasets/{}-data.csv --normalize y'.format(name, name)
    run(cmd, f)

    f = open('./output/k-medoids-{}-unnomalized.csv'.format(name), 'w+')
    cmd = 'python3 ./main.py k-medoids 0 class --attributes datasets/{}-attributes.txt --train datasets/{}-data.csv --normalize n'.format(name, name)
    run(cmd, f)

    f = open('./output/k-medoids-{}-nomalized.csv'.format(name), 'w+')
    cmd = 'python3 ./main.py k-medoids 0 class --attributes datasets/{}-attributes.txt --train datasets/{}-data.csv --normalize y'.format(name, name)
    run(cmd, f)
