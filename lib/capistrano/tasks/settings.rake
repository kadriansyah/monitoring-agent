namespace :setup do
    desc 'Uploading settings.cfg'
    task :settings do
        on roles(:app) do
            upload! StringIO.new(File.read('settings.cfg')), "#{shared_path}/settings/settings.cfg"
            upload! StringIO.new(File.read('bigquery-client-dev.json')), "#{shared_path}/settings/bigquery-client-dev.json"
        end
    end
end