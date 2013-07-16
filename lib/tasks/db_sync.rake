# https://devcenter.heroku.com/articles/heroku-postgres-import-export#export
namespace :db do
  desc "pull down the database from production and overwrite local db"
  task :sync do
    system("heroku pgbackups:capture --expire && \
      curl -ko latest.dump `heroku pgbackups:url` && \
      pg_restore --verbose --clean --no-acl --no-owner -h localhost -U adam -d orq latest.dump")
  end
end
