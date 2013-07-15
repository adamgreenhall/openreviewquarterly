class ChangeColumn < ActiveRecord::Migration
  def up
    change_column :authors, :biography, :text, :limit => nil
  end

  def down
    change_column :authors, :biography, :string, :limit => 255
  end
end
