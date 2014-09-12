class AddPublishedToAuthor < ActiveRecord::Migration
  def up
    add_column :authors, :is_published, :bool, :default => false
    add_column :authors, :is_publisher, :bool, :default => false
    Author.includes(:pieces, :illustrations).each do |a|
      pub = a.pieces.any?{|p| p.issue.is_published}
      pub |= a.illustrations.any?{|p| p.issue.is_published}
      if ['Ahillen', 'Greenhall'].include?(a.last_name) && ['Michael','Amelia','Adam'].include?(a.first_name)
        a.is_publisher = true
      end
      a.is_published = pub
      a.save!
    end
  end
  def down
    remove_column :authors, :is_published, :is_publisher
  end
end
