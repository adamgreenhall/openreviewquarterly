class ChangePieceContent < ActiveRecord::Migration
  def up
    change_column :pieces, :content, :text 
  end

  def down
    change_column :pieces, :content, :string
  end
end
