class DropLimitFromPiecesContent < ActiveRecord::Migration
  def up
    change_column :pieces, :content, :text, :limit => nil
  end

  def down
    change_column :pieces, :content, :text 
  end
end
