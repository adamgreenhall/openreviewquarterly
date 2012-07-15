class CreateIssues < ActiveRecord::Migration
  def change
    create_table :issues do |t|
      t.string :title
      t.integer :number
      t.string :season
      t.boolean :is_published

      t.timestamps
    end
  end
end
