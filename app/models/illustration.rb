class Illustration < ActiveRecord::Base
  belongs_to :piece
  belongs_to :author
  belongs_to :issue
  validates_presence_of :author_id, :piece_id, :issue_id
  attr_accessible :title, :author_id, :piece_id, :issue_id
  def url
    title=(self.title.nil? || self.title=='') ? "untitled" : self.title
    URLify.urlify(title+self.author.name, '-')
  end 
  def nice_name
    (self.title.nil? || self.title=='') ? "Illustration for #{self.piece.nice_name}" : self.title
  end
end
