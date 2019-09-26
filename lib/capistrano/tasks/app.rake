namespace :app do
    desc 'Start Application'
    task :start_dev do
        on roles(:app) do
            execute "nohup /home/grumpycat/anaconda3/envs/monitoring/bin/python -u #{current_path}/monitor_endpoint.py > #{shared_path}/logs/monitor_endpoint.log 2>&1 &"
        end
    end
end

namespace :app do
    desc 'Stop Application'
    task :stop_dev do
        on roles(:app) do
            execute "sudo pkill -f '/home/grumpycat/anaconda3/envs/monitoring/bin/python -u #{current_path}/monitor_endpoint.py'"
        end
    end
end