module ApplicationHelper
  def urlify(name,replaceChar='-')
    URLify.urlify(name,replaceChar)
  end
  def link_to_issue(issue)
    link_to issue.title, urlify(issue.title)
  end
  def link_to_piece(piece,hash_in_issue=false)
    piece_title=piece.nice_name
    if hash_in_issue
      link_to piece_title, '#'+urlify(piece_title), :class=>'toc-hash-link'    #urlify(piece.issue.title)+   
    else
      link_to piece_title, urlify(piece.issue.title)+'/'+urlify(piece_title)
    end
  end
  def link_to_author(author)
    link_to author.name, 'people/'+urlify(author.name)
  end  
end

