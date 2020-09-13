docker run -it --rm \
    -v $PWD/autograde.tar:/home/autolab/autograde.tar:ro \
    -v $PWD/autograde-Makefile:/home/autolab/Makefile:ro \
    -v $PWD/Solution.java:/home/autolab/Solution:ro \
    -v $PWD:/app \
    -w /home/autolab/ \
    --network none \
    --memory 2g \
    --cpus 1 \
    linnil1/judger_java \
    bash
