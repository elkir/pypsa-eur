for  end in {"07","14"};
    do
    for folder in {"add_extra_components","cluster_network","prepare_network","simplify_network","solve_network"};
        do
        mv "$folder/2013-01-$end"/* "2013-01-$end/$folder";
        done;
    done;

for  end in {"07","14"};
    do
    for folder in {"add_extra_components","cluster_network","prepare_network","simplify_network","solve_network"};
        do
        rmdir "$folder/2013-01-$end"
        done;
    done;
    