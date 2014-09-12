class Illustration < ActiveRecord::Base
  belongs_to :piece
  belongs_to :author
  belongs_to :issue
  validates_presence_of :author_id, :piece_id, :issue_id
  attr_accessible :title, :author_id, :piece_id, :issue_id, :url_external
  def url
    if self.url_external.blank?
      "illustrations/#{self.issue.url.gsub('/','')}/"+URLify.urlify("#{self.nice_name}-#{self.author.name}", '-')+".jpg"
    else
      self.url_external
    end
  end
  def nice_name
    (self.title.nil? || self.title=='') ? self.piece.title : self.title
  end
  def is_published
    self.issue.is_published
  end
end
