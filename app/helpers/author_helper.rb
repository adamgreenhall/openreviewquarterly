module AuthorHelper
  def author_photo(author)
    image_tag 'authors/'+urlify(author.name,'_')+'.jpg'
  end
end
