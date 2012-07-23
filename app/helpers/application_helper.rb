module ApplicationHelper
  def urlify(name,replaceChar='-')
    URLify.urlify(name,replaceChar)
  end
  def link_to_issue(issue)
    link_to issue.title, issue.url
  end
  def link_to_piece(piece,hash_in_issue=false)
    piece_title=piece.nice_name
    if hash_in_issue
      link_to piece_title, piece.issue.url+'#'+piece.url, :class=>'toc-hash-link'    #urlify(piece.issue.title)+   
    else
      link_to piece_title, piece.issue.url+'/'+piece.url
    end
  end
  def link_to_author(author)
    link_to author.name, author.url
  end  
end

