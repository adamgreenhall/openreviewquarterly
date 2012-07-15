class AddDescriptionToIssue < ActiveRecord::Migration
  def change
    add_column :issues, :description, :string

  end
end
