class AddUrLtoIllustration < ActiveRecord::Migration
  def up
    add_column :illustrations, :url_external, :string
  end

  def down
    remove_column :illustrations, :url_external
  end
end
