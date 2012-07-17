class AddBioToAuthor < ActiveRecord::Migration
  def change
    add_column :authors, :biography, :string

  end
end
