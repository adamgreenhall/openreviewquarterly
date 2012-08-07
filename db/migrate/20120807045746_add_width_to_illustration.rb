class AddWidthToIllustration < ActiveRecord::Migration
  def change
    add_column :illustrations, :width, :string

  end
end
