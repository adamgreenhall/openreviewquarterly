class CreatePieces < ActiveRecord::Migration
  def change
    create_table :pieces do |t|
      t.string :title
      t.integer :number
      t.integer :author_id
      t.integer :issue_id
      t.string :type

      t.timestamps
    end
  end
end
