class AddSlugToPieces < ActiveRecord::Migration
  def change
    add_column :pieces, :slug, :string
    
    Piece.all.each do |p|
      p.slug = p.get_slug
      p.save
    end
  end
end
