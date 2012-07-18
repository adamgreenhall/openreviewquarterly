class AddDefaultToIssuesIsPublished < ActiveRecord::Migration
  def change
    change_column :issues, :is_published, :boolean, :default => false
  end
end
