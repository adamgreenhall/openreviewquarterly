class AddContentToPiece < ActiveRecord::Migration
  def change
    add_column :pieces, :content, :string

  end
end
