module AuthorHelper
  def author_photo(author)
    begin 
      image_tag 'authors/'+urlify("{author.first_name.split.first} {author.last_name}",'_')+'.jpg'
    rescue
      image_tag 'authors/missing_author_photo.jpg'
    end
  end
end
