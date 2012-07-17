class FixColumnNamePieceType < ActiveRecord::Migration
  def change
    rename_column :pieces, :type, :kind
  end
end
