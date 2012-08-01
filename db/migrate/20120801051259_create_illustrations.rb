class CreateIllustrations < ActiveRecord::Migration
  def change
    create_table :illustrations do |t|
      t.references :piece
      t.references :author
      t.references :issue
      t.string :title

      t.timestamps
    end
    add_index :illustrations, :piece_id
    add_index :illustrations, :author_id
    add_index :illustrations, :issue_id
  end
end
