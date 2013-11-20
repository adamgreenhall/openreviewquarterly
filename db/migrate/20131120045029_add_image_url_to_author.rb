class AddImageUrlToAuthor < ActiveRecord::Migration

  def up
    add_column :authors, :image_url, :string

    Author.all.each do |a|
      a.image_url = 'http://orq.s3.amazonaws.com/authors/'+URLify.urlify("#{a.first_name.split.first} #{a.last_name}",'_')+'.jpg'
      a.save
    end
  end
  
  def down
    remove_column :authors, :image_url
  end
end
