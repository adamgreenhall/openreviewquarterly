class ChangeIssuePromptToText < ActiveRecord::Migration
  def up
    change_column :issues, :prompt, :text, :limit => nil
  end

  def down
    change_column :issues, :prompt, :string
  end
end
