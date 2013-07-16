module ApplicationHelper
  def urlify(name,replaceChar='-')
    URLify.urlify(name,replaceChar)
  end
  def link_to_issue(issue)
    link_to issue.title, issue.url
  end
  def link_to_piece(piece, hash_in_issue=false)
    piece_title = piece.nice_name
    if hash_in_issue
      puts piece_title, piece.slug, piece.title, piece.author.name
      link_to piece_title, piece.issue.url+'#'+piece.slug, :class=>'toc-hash-link'    #urlify(piece.issue.title)+   
    else
      link_to piece_title, piece.issue.url+'/'+piece.slug
    end
  end
  def link_to_author(author)
    link_to author.name, author.url
  end  
end

