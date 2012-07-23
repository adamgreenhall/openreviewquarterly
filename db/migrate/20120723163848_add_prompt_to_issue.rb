class AddPromptToIssue < ActiveRecord::Migration
  def change
    add_column :issues, :prompt, :string

  end
end
