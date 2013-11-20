module AuthorHelper
  def author_photo(author)
    if !author.image_url.empty?
      image_tag author.image_url
    else
      image_tag "http://orq.s3.amazonaws.com/authors/missing_author_photo.jpg"
    end
  end
end
